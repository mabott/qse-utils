#!/usr/bin/env python
# Copyright (c) 2013 Qumulo, Inc.
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

import unittest
import qumulo.lib.opts
import qumulo.rest.kv
from qumulo.rest.rest_test import RestTest

class GetValueRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.kv.get, "GET")

    # Assert a successful request
    def assert_success(self, key, uid, exp_uri):
        self.run_command(key, uid)
        self.assertCalledWith(exp_uri)

    def test_success(self):
        self.assert_success("foo", 500, "/v1/kv/500/foo")

    def test_invalid(self):
        self.assert_request_raises(ValueError, "foo", "abc")

class SetValueRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.kv.put, "PUT")
        self.body = { 'key' : 'foo', 'value' : 'bar' }

    # Assert a successful request
    def assert_success(self, key, value, uid, exp_uri):
        self.run_command(key, value, uid)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "bar", 500, "/v1/kv/500/foo")

    def test_invalid(self):
        self.assert_request_raises(ValueError, "foo", "bar", "abc")

class DeleteValueRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.kv.delete, "DELETE")

    # Assert a successful request
    def assert_success(self, key, uid, exp_uri):
        self.run_command(key, uid)
        self.assertCalledWith(exp_uri)

    def test_success(self):
        self.assert_success("foo", 500, "/v1/kv/500/foo")

    def test_invalid(self):
        self.assert_request_raises(ValueError, "foo", "abc")

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
