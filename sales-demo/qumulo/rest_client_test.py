#!/usr/bin/env python
# Copyright (c) 2014 Qumulo, Inc. All rights reserved.
#
# NOTICE: All information and intellectual property contained herein is the
# confidential property of Qumulo, Inc. Reproduction or dissemination of the
# information or intellectual property contained herein is strictly forbidden,
# unless separate prior written permission has been obtained from Qumulo, Inc.

import qpaths
qpaths.setpaths()

import collections
import os
import socket
import threading
import unittest

import tornado.httpserver
import tornado.ioloop
import tornado.web

import mock

import qinternal.simnode.port_allocator as port_allocator

# Tornado has philosophical differences with pylint
# pylint: disable=abstract-method,arguments-differ
# pylint: disable=attribute-defined-outside-init

ReturnValue = collections.namedtuple('ReturnValue', 'data etag')

class RestClientTest(unittest.TestCase):
    '''
    A small test case to see that the property and request method creation
    functions are working as intended.
    '''
    def setUp(self):
        patcher = mock.patch('qumulo.rest.fs.create_link')
        self.addCleanup(patcher.stop)
        self.mock_create_link = patcher.start()
        self.mock_create_link.__name__ = 'create_link'
        self.mock_create_link.return_value = \
                ReturnValue({'key': 'value'}, 'md5')

        patcher = mock.patch('qumulo.rest.auth.login')
        self.addCleanup(patcher.stop)
        self.mock_login = patcher.start()
        self.mock_login.__name__ = 'login'
        self.mock_login.return_value = ReturnValue({
            'issue': 44,
            'key': 'key',
            'key_id': 'key_id',
            'algorithm': 'algorithm'
        }, 'etag')

    def test_fs_create_link(self):
        import qinternal.cli.qumulo.rest_client as rest_client
        rc = rest_client.RestClient('hostname', port=42)
        result = rc.fs.create_link('foo', 'bar', dir_id=97)
        self.mock_create_link.assert_called_once_with(
            rc.conninfo, rc.credentials, 'foo', 'bar', dir_id=97)

        self.assertEqual(result['key'], 'value')

        self.assertEqual([], self.mock_login.call_args_list)

    def test_with_login(self):
        import qinternal.cli.qumulo.rest_client as rest_client
        rc = rest_client.RestClient('hostname', 1034)
        rc.login('user', 'pass')
        self.assertEqual(rc.credentials.issue, 44)

class FakeRestServer(object):
    def __init__(self, port, block):
        class Handler(tornado.web.RequestHandler):
            def initialize(self, response, block):
                self.response = response
                self.block = block

            def get(self, *args):
                if block:
                    block.wait()
                self.write(self.response)
                self.set_header('Content-Type', 'application/json')

        self.response = {u'hi': u'there'}
        app = tornado.web.Application([
            (r"/(.*)", Handler, { 'response': self.response, 'block': block})])
        src_root = qpaths.find_src_root()
        certfile = os.path.join(src_root, 'keys/eng.qumulo.com.crt')
        keyfile = os.path.join(src_root, 'keys/eng.qumulo.com.key')
        ssl_options = { "certfile": certfile, "keyfile": keyfile }
        server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_options)
        server.listen(port)
        self.io_loop = tornado.ioloop.IOLoop.instance()
        self.thread = threading.Thread(target=self.io_loop.start)
        self.thread.start()

    def stop(self):
        self.io_loop.stop()
        self.thread.join()

class FakeRestServerTest(unittest.TestCase):
    def test_server(self):
        port = port_allocator.allocate_port(os.environ['TMPDIR'])
        server = FakeRestServer(port, None)

        import qinternal.cli.qumulo.rest_client as rest_client
        rc = rest_client.RestClient('localhost', port=port)
        self.assertEqual(rc.version.version(), {u'hi': u'there'})

        server.stop()

class RestClientTimeoutTest(unittest.TestCase):
    '''
    Test cases to ensure the timeout functionality works as intended.
    '''
    def test_connect_timeout(self):
        import qinternal.cli.qumulo.rest_client as rest_client
        # Unreachable Test-Net ip from RFC-3330
        ipaddr = '192.0.2.1'
        rc = rest_client.RestClient(ipaddr, port=42, timeout=1)
        self.assertRaises(socket.timeout, rc.auth.login, 'admin', 'admin')

    def test_handshake_timeout(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = port_allocator.allocate_port(os.environ['TMPDIR'])
        server.bind(('localhost', port))
        server.listen(10)

        import qinternal.cli.qumulo.rest_client as rest_client
        rc = rest_client.RestClient('localhost', port=port, timeout=1)
        self.assertRaisesRegexp(socket.error, r'timed out', rc.version.version)

    def test_read_timeout(self):
        port = port_allocator.allocate_port(os.environ['TMPDIR'])
        block = threading.Event()
        server = FakeRestServer(port, block)

        import qinternal.cli.qumulo.rest_client as rest_client
        rc = rest_client.RestClient('localhost', port=port, timeout=1)
        self.assertRaisesRegexp(socket.error, r'timed out', rc.version.version)

        block.set()
        server.stop()

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
