#!/usr/bin/env python
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

import unittest
import mock
import qumulo.lib.opts
import qumulo.rest.fs
from qumulo.rest.rest_test import RestTest
from qumulo.lib.request import CONTENT_TYPE_BINARY

class GetAttrRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.get_attr, "GET")

    def assert_success(self, exp_uri, path=None, id_=None):
        self.run_command(path=path, id_=id_)
        self.assertCalledWith(exp_uri)

    def test_success(self):
        self.assert_success("/v1/fs/path/%2Ffoo?attributes", path="foo")
        self.assert_success("/v1/fs/id/1?attributes", id_="1")

    def test_empty_path(self):
        self.run_command("")
        self.assertCalledWith("/v1/fs/path/%2F?attributes")

class SetAttrRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.set_attr, "PUT")
        self.mode = 'hung over'
        self.owner = 'Jeff Daniels'
        self.group = 'Bad Whiskey'
        self.size = 'far too large'
        self.modification_time = 'recent'
        self.change_time = 'dunno'
        self.body = {
            'mode': self.mode,
            'owner': self.owner,
            'group': self.group,
            'size': self.size,
            'modification_time': self.modification_time,
            'change_time': self.change_time,
        }
        self.if_match = 'etag'

    def test_success(self):
        self.run_command(self.mode, self.owner, self.group, self.size,
            self.modification_time, self.change_time, "foo", None,
            self.if_match)
        self.assertCalledWith("/v1/fs/path/%2Ffoo?attributes",
            body=self.body, if_match=self.if_match)

    def test_success_by_id(self):
        self.run_command(self.mode, self.owner, self.group, self.size,
            self.modification_time, self.change_time, None, "1", self.if_match)
        self.assertCalledWith("/v1/fs/id/1?attributes",
            body=self.body, if_match=self.if_match)

    def test_empty_path(self):
        self.run_command(self.mode, self.owner, self.group, self.size,
            self.modification_time, self.change_time, "", None, self.if_match)
        self.assertCalledWith("/v1/fs/path/%2F?attributes",
            body=self.body, if_match=self.if_match)

class SetFileAttrRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.set_file_attr, "PATCH")
        self.mode = 'chipper'
        self.owner = 'Pizza Hut'
        self.group = 'Food-ish'
        self.size = '15 inches'
        self.creation_time = 'Under 30 min'
        self.modification_time = 'Chewed recently'
        self.change_time = 'Subject to digestion'
        self.body = {
            'mode': self.mode,
            'owner': self.owner,
            'group': self.group,
            'size': self.size,
            'creation_time': self.creation_time,
            'modification_time': self.modification_time,
            'change_time': self.change_time,
        }
        self.if_match = 'Want pizza'

    def test_success(self):
        self.run_command(self.mode, self.owner, self.group, self.size,
            self.creation_time, self.modification_time, self.change_time, "2",
            self.if_match)
        self.assertCalledWith("/v1/fs/file/2/attributes",
            body=self.body, if_match=self.if_match)

ACL_QUERY = [('acl', None)]

class GetAclRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.get_acl, "GET")

    def assert_success(self, exp_uri, path=None, id_=None):
        self.run_command(path=path, id_=id_)
        self.assertCalledWith(exp_uri)

    def test_success(self):
        self.assert_success("/v1/fs/path/%2Ffoo?acl", path="foo")
        self.assert_success("/v1/fs/id/1?acl", id_="1")

    def test_empty_path(self):
        self.run_command("")
        self.assertCalledWith("/v1/fs/path/%2F?acl")

class SetAclRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.set_acl, "PUT")

    def test_acl(self):
        aces = ['wild', 'mild', 'jacky']
        control = ['none', 'some', 'freak']
        body = {'control': control, 'aces': aces}
        if_match = '!'
        self.run_command(path="foo", aces=aces, control=control,
                         if_match=if_match)
        self.assertCalledWith("/v1/fs/path/%2Ffoo?acl", body=body,
                              if_match=if_match)
        self.run_command(id_="1", aces=aces, control=control, if_match=if_match)
        self.assertCalledWith("/v1/fs/id/1?acl", body=body, if_match=if_match)

    def test_only_one(self):
        aces = mock.Mock()
        if_match = mock.Mock()
        control = mock.Mock()
        self.assert_request_raises(ValueError, path="foo", aces=aces,
                if_match=if_match)

        self.assert_request_raises(ValueError, path="foo", control=control,
                if_match=if_match)

    def test_neither(self):
        if_match = mock.Mock()
        self.assert_request_raises(ValueError, path="foo", if_match=if_match)

class CreateFileRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.create_file, "POST")
        self.body = { 'name': 'foo', 'action': 'CREATE_FILE' }

    # Assert a successful request
    def assert_success(self, name, exp_uri, dir_path=None, dir_id=None):
        self.run_command(name, dir_path, dir_id)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")

        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="bar/")
        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="/bar/")

        self.assert_success("foo", "/v1/fs/id/1", dir_id="1")

    def test_corrected_name(self):
        self.assert_success("foo/", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")

class CreateDirectoryRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.create_directory, "POST")
        self.body = { 'name': 'foo', 'action': 'CREATE_DIRECTORY' }

    # Assert a successful request
    def assert_success(self, name, exp_uri, dir_path=None, dir_id=None):
        self.run_command(name, dir_path, dir_id)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")

        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="bar/")
        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="/bar/")

        self.assert_success("foo", "/v1/fs/id/1", dir_id="1")

class CreateSymlinkRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.create_symlink, "POST")
        self.target = 'slash bar'
        self.body = { 'name': 'foo',
                      'old_path': self.target,
                      'action': 'CREATE_SYMLINK' }

    # Assert a successful request
    def assert_success(self, name, exp_uri, dir_path=None, dir_id=None):
        self.run_command(name, self.target, dir_path, dir_id)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")

        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="bar/")
        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="/bar/")

        self.assert_success("foo", "/v1/fs/id/1", dir_id="1")

    def test_corrected_name(self):
        self.assert_success("foo/", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")

class CreateLinkRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.create_link, "POST")
        self.target = 'whatever'
        self.body = { 'name': 'foo',
                      'old_path': self.target,
                      'action': 'CREATE_LINK' }

    # Assert a successful request
    def assert_success(self, name, exp_uri, dir_path=None, dir_id=None):
        self.run_command(name, self.target, dir_path, dir_id)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")

        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="bar/")
        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="/bar/")

        self.assert_success("foo", "/v1/fs/id/1", dir_id="1")

    def test_corrected_name(self):
        self.assert_success("foo/", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")

class RenameRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.rename, "POST")
        self.source = 'Lake Victoria'
        self.body = {'name': 'foo', 'old_path': self.source, 'action': 'RENAME'}

    # Assert a successful request
    def assert_success(self, name, exp_uri, dir_path=None, dir_id=None):
        self.run_command(name, self.source, dir_path, dir_id)
        self.assertCalledWith(exp_uri, body=self.body)

    def test_success(self):
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo", "/v1/fs/path/%2F", dir_path="/")

        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="bar/")
        self.assert_success("foo", "/v1/fs/path/%2Fbar%2F", dir_path="/bar/")

        self.assert_success("foo", "/v1/fs/id/1", dir_id="1")

    def test_corrected_name(self):
        self.assert_success("foo/", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")
        self.assert_success("foo//", "/v1/fs/path/%2F", dir_path="/")

class DeleteRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.delete, "DELETE")

    def test_success(self):
        self.run_command("foo")
        self.assertCalledWith("/v1/fs/path/%2Ffoo")

    def test_empty_path(self):
        self.run_command("")
        self.assertCalledWith("/v1/fs/path/%2F")

class WriteFileRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.write_file, "PUT")

    def assert_success(self, path, id_, exp_uri):
        body_file = mock.Mock()
        if_match = 'a condition'
        self.run_command(body_file, path, id_, if_match)
        self.assertCalledWith(exp_uri, body_file=body_file, if_match=if_match,
            request_content_type=CONTENT_TYPE_BINARY)

    def test_success(self):
        self.assert_success("foo", None, "/v1/fs/path/%2Ffoo")
        self.assert_success(None, "1", "/v1/fs/id/1")
        self.assert_success("", None, "/v1/fs/path/%2F")

class ReadFileRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.read_file, "GET")

    def assert_success(self, exp_uri, path=None, id_=None):
        response_file = mock.Mock()
        self.run_command(response_file, path=path, id_=id_)
        self.assertCalledWith(exp_uri, response_file=response_file,
            response_content_type=CONTENT_TYPE_BINARY)

    def test_success(self):
        self.assert_success("/v1/fs/path/%2Ffoo", path="foo")
        self.assert_success("/v1/fs/path/%2F", path="")
        self.assert_success("/v1/fs/id/1", id_="1")

class ReadDirRestTest(unittest.TestCase, RestTest):
    def setUp(self):
        RestTest.setUp(self, qumulo.rest.fs.read_directory, "GET")

    def assert_success(self, exp_uri, page_size, path=None, id_=None):
        self.run_command(page_size, path=path, id_=id_)
        self.assertCalledWith(exp_uri)

    def test_success(self):
        self.assert_success("/v1/fs/path/%2Ffoo%2F?readdir&limit=10", 10,
            path="foo")
        self.assert_success("/v1/fs/id/1?readdir&limit=50", 50, id_="1")

    def test_empty_path(self):
        self.assert_success("/v1/fs/path/%2F?readdir&limit=10", 10, path="")

    def test_no_page_size(self):
        self.assert_success("/v1/fs/path/%2Ffoo%2F?readdir", None, path="foo")

class ReadEntireDirectoryTest(unittest.TestCase):
    CALL_DATA = [
        {
            "child_count": 3,
            "files": [
                { "name": "file1" },
                { "name": "file2" },
                { "name": "file3" },
            ],
            "id": 2,
            "paging": {
                "next": "OPAQUE_PAGE_2_URL",
                "prev": ""
            },
            "path": "/"
        },
        {
            "child_count": 3,
            "files": [
                { "name": "file4" },
                { "name": "file5" },
                { "name": "file6" },
            ],
            "id": 2,
            "paging": {
                "next": "OPAQUE_PAGE_3_URL",
                "prev": "OPAQUE_PAGE_1_URL"
            },
            "path": "/"
        },
        {
            "child_count": 2,
            "files": [
                { "name": "file7" },
                { "name": "file8" },
            ],
            "id": 2,
            "paging": {
                "next": "",
                "prev": "OPAQUE_PAGE_2_URL"
            },
            "path": "/"
        },
    ]
    ALL_FILE_NAMES = [
        "file1",
        "file2",
        "file3",
        "file4",
        "file5",
        "file6",
        "file7",
        "file8",
    ]

    def setUp(self):
        self.func = qumulo.rest.fs.read_entire_directory

        # Mock these to make sure they are passed through
        self.conninfo = mock.Mock()
        self.credentials = mock.Mock()

        # Set up mock for rest_request
        request_patcher = mock.patch('qumulo.lib.request.rest_request',
            side_effect=self.rest_request)
        self.request_mock = request_patcher.start()
        self.addCleanup(request_patcher.stop)

        self.expected_uri = None

    def rest_request(self, _cred, _conn, method, uri, **kwargs):
        self.assertEqual(method, "GET")
        self.assertEqual(uri, self.expected_uri)
        self.assertEqual(kwargs, {})

        # Make sure we didn't go past the end
        self.assertTrue(self.expected_uri)

        # Call count is one the first time we're called.  Look up the call data
        call_data_index = self.request_mock.call_count - 1
        call_data = self.CALL_DATA[call_data_index]
        self.assertIsNotNone(call_data)

        # Set the expecte URI for the next time around
        self.expected_uri = call_data['paging']['next']

        # Return the data in a response object
        return mock.MagicMock(data=call_data)

    def run_generator(self, expected_initial_uri, **kwargs):
        # Set the initial URI
        self.expected_uri = expected_initial_uri

        # Read the directory, gathering the filenames as we iterate
        file_names = []
        for data in self.func(self.conninfo, self.credentials, **kwargs):
            for file_item in data['files']:
                file_names.append(file_item['name'])

        # Check we were called the right number of times, and saw all the files
        self.assertEqual(self.request_mock.call_count, len(self.CALL_DATA))
        self.assertEqual(file_names, self.ALL_FILE_NAMES)

    def test_path(self):
        self.run_generator("/v1/fs/path/%2F?readdir", path="/")

    def test_path_with_page_size(self):
        self.run_generator(
            "/v1/fs/path/%2F?readdir&limit=10", page_size=10, path="/")

    def test_id(self):
        self.run_generator("/v1/fs/id/2?readdir", id_=2)

    def test_id_and_page_size(self):
        self.run_generator("/v1/fs/id/2?readdir&limit=10", id_=2, page_size=10)

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
