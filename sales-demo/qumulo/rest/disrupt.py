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

import qumulo.lib.request as request
from qumulo.lib.uri import UriBuilder

@request.request
def panic(conninfo, credentials):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/disrupt/panic"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def rpc_glitch(conninfo, credentials, remote):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/disrupt/rpc_glitch"))
    body = { 'id' : int(remote) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def rpc_disconnect(conninfo, credentials, remote):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/disrupt/rpc_disconnect"))
    body = { 'id' : int(remote) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def rpc_reconnect(conninfo, credentials, remote):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/disrupt/rpc_reconnect"))
    body = { 'id' : int(remote) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def sleep(conninfo, credentials, seconds):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/disrupt/sleep"))
    body = { 'seconds' : int(seconds) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)
