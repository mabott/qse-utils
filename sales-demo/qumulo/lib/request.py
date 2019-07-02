# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import collections
import cStringIO
import errno
import httplib
import json
import os
import random
import socket
import sys
import ssl

import qumulo.lib.log as log

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_BINARY = "application/octet-stream"

DEFAULT_CHUNKED = False
DEFAULT_CHUNK_SIZE_BYTES = 1024

NEED_LOGIN_MESSAGE = \
    "Need to log in first to establish credentials."

PRIV_PORT_BEG = 900
PRIV_PORT_END = 1024

# Decorator for request methods
def request(fn):
    fn.request = True
    return fn

def pretty_json(obj):
    return json.dumps(obj, sort_keys=True, indent=4)

def stream_writer(conn, file_):
    chunk_size = 128*1024
    while True:
        data = conn.read(chunk_size)
        if len(data) == 0:
            return
        file_.write(data)

class HTTPSConnectionWrapped(httplib.HTTPSConnection):

    # JIRA-4939 timeout value (seconds).
    MACOS_SOCKET_BUG_WORKAROUND_TIMEOUT = 20

    def connect(self):

        # JIRA-4939: Bug in MacOS sockets.
        #
        # There exists a bug in the MacOS 10.9 socket stack where unaccepted
        # child sockets are not properly reset / closed when the listening
        # socket is closed (during a restart of the HTTP server).
        #
        # This leaves the client waiting on a response from a socket which
        # hasn't been accepted, and can never be accepted, at the other end,
        # until the entire client test times out.
        #
        # The way we work around this is to set a timeout on the underlying
        # socket whilst waiting for a response to our original request (the
        # connect() and initial send() succeed because the kernel TCP stack
        # handles this much), and catch the timeout at a higher level where
        # we can retry the request.
        #
        # This is a nasty hack. We should really stopping pushing this crap
        # into the codebase just to support a non-production development
        # platform.

        if sys.platform != 'darwin':
            return httplib.HTTPSConnection.connect(self)

        old_timeout = self.timeout

        if not old_timeout:
            self.timeout = self.MACOS_SOCKET_BUG_WORKAROUND_TIMEOUT

        while True:
            # Let connection timeouts propagate back to the caller, but
            # catch any encountered during the SSL handshake.
            # We're really just replicating the code in
            # HTTPSConnection.connect() here (both lines of it).

            sock = socket.create_connection((self.host, self.port),
                                            self.timeout, self.source_address)

            try:
                self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file)
            except socket.timeout:
                log.info("JIRA-4939 during HTTPS connect, retrying...")
            else:
                break

        self.timeout = old_timeout
        self.sock.settimeout(old_timeout
            if old_timeout != socket._GLOBAL_DEFAULT_TIMEOUT else None)

class Connection(object):
    def __init__(self, host, port, chunked=DEFAULT_CHUNKED,
            chunk_size=DEFAULT_CHUNK_SIZE_BYTES, timeout=None):
        self.scheme = 'https'
        self.host = host
        self.port = port
        self.chunked = chunked
        self.chunk_size = chunk_size
        self.conn = None
        self.backdoor = host == 'localhost' and os.geteuid() == 0
        self.timeout = timeout

    def connect_backdoor(self):
        ports = range(PRIV_PORT_BEG, PRIV_PORT_END)
        random.shuffle(ports)

        last_error = socket.error('Disable raising-bad-type')
        for port in ports:
            try:
                conn = HTTPSConnectionWrapped(
                        self.host, self.port,
                        source_address=('localhost', port),
                        timeout=self.timeout)
                conn.connect()
                return conn
            except socket.error as e:
                last_error = e
        # If we tried all the ports, we'll bail out with the last error we got
        # which is likely a connection refused error meaning the server
        # is not up.  A little lame that we go through all the ports to
        # determine this, but it's quick.
        raise last_error

    def connect(self):
        if self.backdoor and self.conn:
            # Need to close the connection to get a new local priv port, the one
            # stuck in the conn is probably in TIME_WAIT.
            self.conn = None
        if self.conn is None:
            if self.backdoor:
                self.conn = self.connect_backdoor()
            else:
                self.conn = HTTPSConnectionWrapped(
                    self.host, self.port, timeout=self.timeout)

        return self.conn

    def reconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

        return self.connect()

class APIException(Exception):
    '''Unusual errors when sending request or receiving response.'''
    pass

class RequestError(Exception):
    '''An error response to an invalid REST request. A combination of HTTP
    status code, HTTP status message and REST error response.'''

    def __init__(self, status_code, status_message, json_error):
        self.status_code = status_code
        self.status_message = status_message

        try:
            self.module = json_error['module']
            self.error_class = json_error['error_class']
            self.description = json_error['description']
            self.stack = json_error['stack']
            self.user_visible = json_error['user_visible']
        except Exception:
            # Error: Create fake json error fields
            # XXXEEY: lame to manually concoct an error message
            if status_code == 401:
                self.description = NEED_LOGIN_MESSAGE
            else:
                self.description = "Dev error: No json error response."

            self.module = 'qumulo.lib.request'
            self.error_class = 'unknown'
            self.stack = ''

        message = "Error %d: %s: %s" % (self.status_code, self.error_class,
            self.description)
        Exception.__init__(self, message)

#  ____                            _
# |  _ \ ___  __ _ _   _  ___  ___| |_
# | |_) / _ \/ _` | | | |/ _ \/ __| __|
# |  _ <  __/ (_| | |_| |  __/\__ \ |_
# |_| \_\___|\__, |\__,_|\___||___/\__|
#               |_|

class APIRequest(object):
    '''REST API request class.'''

    # Error responses should be JSON.
    ERROR_RESPONSE_CONTENT_TYPE = CONTENT_TYPE_JSON

    def __init__(self, conninfo, credentials, method, uri,
            body=None, body_file=None,
            if_match=None, request_content_type=CONTENT_TYPE_JSON,
            response_content_type=CONTENT_TYPE_JSON, response_file=None,
            headers=None):
        self.conninfo = conninfo
        self.credentials = credentials
        self.method = method
        self.uri = uri
        self.chunked = conninfo.chunked
        self.chunk_size = conninfo.chunk_size
        self.response = None
        self.response_etag = None
        self._response_data = None
        self.response_obj = None
        self.conn = self.conninfo.connect()
        self._headers = collections.OrderedDict()
        self._headers.update(headers or {})
        if if_match is not None:
            self._headers['If-Match'] = if_match

        # Request type defaults to JSON. If overridden, body_file is required.
        self.request_content_type = request_content_type
        if request_content_type is not CONTENT_TYPE_JSON:
            assert body_file is not None, "Binary request requires body_file"

        # Response type defaults to JSON, but can be overridden.
        # A binary response must pass in a file to output to.
        self.response_content_type = response_content_type
        self.response_file = response_file
        if response_content_type == CONTENT_TYPE_BINARY:
            assert response_file is not None, \
                "Binary response requires file object"

        self.body_text = None
        self.body_file = None
        self.body_length = 0
        if body_file is not None:
            self.body_file = body_file

            # Most http methods want to overwrite fully, so seek to 0.
            if not method == "PATCH":
                body_file.seek(0, 0)

            current_pos = body_file.tell()
            body_file.seek(0, 2)
            self.body_length = body_file.tell() - current_pos
            body_file.seek(current_pos, 0)

        elif body is not None:
            self.body_text = body
            self.body_file = cStringIO.StringIO(self._body_text())
            self.body_length = len(self._body_text())

    def send_request(self):
        self._headers["Content-Type"] = self.request_content_type

        if self.chunked:
            self._headers['Transfer-Encoding'] = "chunked"
        else:
            self._headers['Content-Length'] = self.body_length

        if self.credentials:
            request_info = {
                'scheme' : self.conninfo.scheme,
                'host' : self.conninfo.host,
                'port' : str(self.conninfo.port),
                'method' : self.method,
                'uri' : self.uri,
                'content_length': self.body_length,
                'body' : self._body_text(),
                'content_type' : self.request_content_type,
            }
            self._headers['Authorization'] = \
                self.credentials.auth_header(**request_info)

        log.debug("REQUEST: {method} {scheme}://{host}:{port}{uri}".format(
            method=self.method, scheme=self.conninfo.scheme,
            host=self.conninfo.host, port=self.conninfo.port,
            uri=self.uri))

        log.debug("REQUEST HEADERS:")
        for header in self._headers:
            log.debug("    %s: %s" % (header, self._headers[header]))

        if (self.body_length > 0):
            log.debug("REQUEST BODY:")
            if (self.request_content_type == CONTENT_TYPE_BINARY):
                log.debug(
                    "\tContent elided. File info: %s (%d bytes)" %
                    (self.body_file, self.body_length))
            else:
                log.debug(pretty_json(self._body_text(False)))
                self.body_file.seek(0)

        # Wrap any random errors in a HttpException to make them more palatable.
        try:
            if self.conn.sock is None:
                self.conn.connect()
        except ssl.SSLError as e:
            # If we see the SSL error "EOF occurred in violation of protocol",
            # we want to add more information, to help with better diagnosis.
            # See QFS-5396.
            if e.errno == ssl.SSL_ERROR_EOF:
                e.strerror = "{} - check server logs for cause (e.g. qfsd)"\
                    .format(e.strerror)

            # Re-raise, preserving the stack
            raise e, None, sys.exc_info()[2]
        except (httplib.HTTPException, socket.error):
            # Already an HTTPException, so just raise it and socket errors are
            # cool too.
            raise
        except Exception as e:
            # Wrap it, but save the type, message, and stack.
            message = os.strerror(e.errno) if hasattr(e, 'errno') else e.message
            wrap = httplib.HTTPException("{}: {}".format(sys.exc_info()[0],
                                                         message))
            raise wrap, None, sys.exc_info()[2]

        try:
            self.conn.putrequest(self.method, self.uri)

            for name, value in self._headers.items():
                self.conn.putheader(name, value)

            self.conn.endheaders()

            # Chunked transfer encoding. Details:
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec3.html#sec3.6.1
            # On our server side chunks are processed by chunked_xfer_istream.h
            if self.chunked:
                if self.body_file is not None:
                    chunk = self.body_file.read(self.chunk_size)
                    while (len(chunk) > 0):
                        self.conn.send("%x\r\n%s\r\n" % (len(chunk), chunk))
                        log.debug("Sent chunk (%u bytes)" % len(chunk))
                        chunk = self.body_file.read(self.chunk_size)
                self.conn.send("0\r\n\r\n")
                log.debug("Sent final chunk")
            elif self.body_file is not None:
                self.conn.send(self.body_file)

        except socket.error as e:
            # Allow EPIPE, server probably sent us a response before breaking
            if e.errno != errno.EPIPE:
                raise

    def get_response(self):
        self.response = self.conn.getresponse()
        self.response_etag = self.response.getheader('etag')

        log.debug("RESPONSE STATUS: %d" % self.response.status)
        # Redirect redirect to auth required for cli
        if self.response.status == 307:
            log.debug("Server replied: %d %s, translating to 401" % (
                    self._status(), self._reason()))
            self.response.status = 401

        # Ensure we have the correct content-type
        content_type = self.response.getheader('content-type')
        length = self.response.getheader('content-length')
        log.debug("RESPONSE LENGTH = %s" % length)
        expected_type = self.response_content_type if self._success() else \
            self.ERROR_RESPONSE_CONTENT_TYPE
        if length != "0" and content_type != expected_type:
            log.debug("Unexpected content-type of %s for length %s" %
                (content_type, length))
            if content_type in (CONTENT_TYPE_JSON, None):
                log.debug(self.response.getheaders())
                log.debug(self.response.read())
            self.conn.close()
            raise APIException("Unexpected content-type of %s for length %s" %
                (content_type, length))

        if self.response_file is None or not self._success():
            self._response_data = self.response.read()
        else:
            stream_writer(self.response, self.response_file)

        self.conn.close()

        if not self._success():
            log.debug("Server replied: %d %s" % (self._status(),
                self._reason()))

        if self._response_data and length != "0":
            try:
                self.response_obj = json.loads(self._response_data)
            except ValueError, e:
                if self._response_data:
                    raise APIException("Error loading data: %s" % str(e))
            else:
                log.debug("RESPONSE:")
                log.debug(self.response.msg)
                if self.response_obj is not None:
                    log.debug("\n" + pretty_json(self.response_obj))
                else:
                    log.debug("<no response body>")

        if not self._success():
            raise RequestError(self._status(), self._reason(),
                self.response_obj)

    def _body_text(self, encoded=True):
        if self.body_text is not None:
            if encoded:
                return json.dumps(self.body_text).encode('utf8')
            else:
                return self.body_text
        else:
            return None

    def _status(self):
        return self.response.status

    def _success(self):
        return self._status() >= 200 and self._status() < 300

    def _reason(self):
        return self.response.reason

#  ____
# |  _ \ ___  ___ _ __   ___  _ __  ___  ___
# | |_) / _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \
# |  _ <  __/\__ \ |_) | (_) | | | \__ \  __/
# |_| \_\___||___/ .__/ \___/|_| |_|___/\___|
#                |_|

class RestResponse(collections.namedtuple('RestResponse', 'data etag')):
    def __str__(self):
        return pretty_json(self.data)

    def lookup(self, key):
        if self.data is not None and key in self.data:
            return self.data[key]
        else:
            raise AttributeError(key)

def rest_request(conninfo, credentials, method, uri, *args, **kwargs):
    rest = APIRequest(conninfo, credentials, method, uri, *args, **kwargs)
    rest.send_request()
    rest.get_response()
    return RestResponse(rest.response_obj, rest.response_etag)
