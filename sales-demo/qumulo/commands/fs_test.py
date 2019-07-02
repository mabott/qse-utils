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
import copy
import mock
import qumulo.lib.request as request
import qumulo.commands.fs
from qumulo.commands.test_mixin import CommandTest

class GetAttrCommandTest(unittest.TestCase, CommandTest):
    def setUp(self):
        CommandTest.setUp(self, qumulo.commands.fs.GetAttrCommand,
            'fs_get_attr', 'qumulo.rest.fs.get_attr')

    def test_arguments(self):
        '--id xor --path must be set and have a value.'
        self.assert_command_raises(ValueError)
        self.assert_command_raises(ValueError, "--path", "foo", "--id", "2")
        self.assert_missing_value('--path')
        self.assert_missing_value('--id')

    def test_extra_argument(self):
        'No positional arguments are allowed.'
        self.assert_extra_argument('--path', 'foo', 'bar')

    def test_success(self):
        resp = { 'foo': 'bar' }
        self.mock.get_attr.return_value = \
            request.RestResponse(resp, 'etag-1')
        self.assert_command_outputs(resp, '--path', 'foo')
        self.assert_call_list(
            mock.call.get_attr(self.conninfo, self.credentials,
                'foo', None))

    def test_rest_failure(self):
        'The command should propogate the exception cleanly.'
        self.mock.get_attr.side_effect = self.request_error
        self.assert_command_raises(request.RequestError, '--path', 'foo')
        self.assert_call_list(
            mock.call.get_attr(self.conninfo, self.credentials,
                'foo', None))

class SetAttrCommandTest(unittest.TestCase, CommandTest):
    def setUp(self):
        CommandTest.setUp(self, qumulo.commands.fs.SetAttrCommand,
            'fs_set_attr', 'qumulo.rest.fs.get_attr',
            'qumulo.rest.fs.set_attr')

        self.attributes = {
            'mode':                      'mode-1',
            'owner':                     'owner-1',
            'group':                     'group-1',
            'size':                      'size-1',
            'modification_time':         'mod-time-1',
            'change_time':               'change-time-1',
        }

        # get_attr just returns self.attributes
        self.mock.get_attr.return_value = \
            request.RestResponse(self.attributes, 'etag-1')

        # set_attr just returns what it was given
        def set_attr(_conninfo, _credentials, mode, owner, group, size,
                modification_time, change_time, _path, _id_, _etag):
            attributes = {
                'mode': mode,
                'owner': owner,
                'group': group,
                'size': size,
                'modification_time': modification_time,
                'change_time': change_time,
            }

            return request.RestResponse(attributes, 'etag-2')
        self.mock.set_attr.side_effect = set_attr

    def test_arguments(self):
        '--id xor --path must be set and have a value.'
        self.assert_command_raises(ValueError)
        self.assert_command_raises(ValueError, "--path", "foo", "--id", "2")
        self.assert_missing_value('--path')
        self.assert_missing_value('--id')

    def test_no_attributes(self):
        'At least one attribute must be set.'
        self.assert_command_raises(ValueError, '--path', 'foo')

    def test_extra_argument(self):
        'No positional arguments are allowed.'
        self.assert_extra_argument('--path', 'foo', 'bar')

    def test_missing_attribute_arguments(self):
        'All attribute options require values.'
        self.assert_missing_value('--mode',                 '--path', 'foo')
        self.assert_missing_value('--owner',                '--path', 'foo')
        self.assert_missing_value('--group',                '--path', 'foo')
        self.assert_missing_value('--size',                 '--path', 'foo')
        self.assert_missing_value('--modification-time',    '--path', 'foo')
        self.assert_missing_value('--change-time',          '--path', 'foo')

    def test_change_mode(self):
        '''
        Test changing only the mode.

        This allows us to test that the other attributes are passed back
        properly.
        '''

        new_attributes = dict(self.attributes)
        new_attributes['mode'] = '664'
        self.assert_command_outputs(new_attributes, '--path', 'foo',
            '--mode', '664')
        self.assert_call_list(
            mock.call.get_attr(self.conninfo, self.credentials, 'foo'),
            mock.call.set_attr(self.conninfo, self.credentials,
                new_attributes['mode'], new_attributes['owner'],
                new_attributes['group'], new_attributes['size'],
                new_attributes['modification_time'],
                new_attributes['change_time'],
                'foo', None, 'etag-1'))

    def test_change_all(self):
        '''
        Test changing all the attributes at once.

        Here we test that all attributes are in fact set by the appropriate
        option string.
        '''

        new_attributes = dict(self.attributes)
        new_attributes['mode'] = '2'
        new_attributes['owner'] = 'owner-2'
        new_attributes['group'] = 'group-2'
        new_attributes['size'] = 'size-2'
        new_attributes['modification_time'] = 'mod-time-2'
        new_attributes['change_time'] = 'change-time-2'
        self.assert_command_outputs(new_attributes, '--path', 'foo',
            '--mode', '2',
            '--owner', 'owner-2',
            '--group', 'group-2',
            '--size', 'size-2',
            '--modification-time', 'mod-time-2',
            '--change-time', 'change-time-2')

    def test_get_error(self):
        '''
        Test get_attr throwing an exception.

        The command should allow the exception to propogate unmolested.
        Additionally, set_attribute should not be called.
        '''

        self.mock.get_attr.side_effect = self.request_error
        self.assert_command_raises(request.RequestError, '--path', 'foo',
            '--mode', '2')
        self.assert_call_list(
            mock.call.get_attr(self.conninfo, self.credentials, 'foo'))

    def test_set_error(self):
        '''Test set_attr throwing an exception.'''

        self.mock.set_attr.side_effect = self.request_error
        self.assert_command_raises(request.RequestError, '--path', 'foo',
            '--mode', '2')
        self.assert_call_list(
            mock.call.get_attr(self.conninfo, self.credentials, 'foo'),
            mock.call.set_attr(self.conninfo, self.credentials,
                mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY, mock.ANY,
                'foo', None, 'etag-1'))

class ReadDirectoryTest(unittest.TestCase, CommandTest):
    def setUp(self):
        CommandTest.setUp(self, qumulo.commands.fs.ReadDirectoryCommand,
            'fs_read_dir', 'qumulo.rest.fs.read_directory',
            'qumulo.lib.request.rest_request')

    def test_paginated_read(self):
        # mock out response that requires more pages (actual JSON content
        # is otherwise irrelevant here)
        paging_response = {
            'paging': {'next': '/v1/something' },
            'files': ['foobar'],
            'path': '/'
        }
        self.mock.read_directory.return_value = \
            request.RestResponse(paging_response, 'etag-1')

        # mock out final response where next is empty
        last_response = copy.deepcopy(paging_response)
        last_response['paging']['next'] = ''
        self.mock.rest_request.return_value = \
            request.RestResponse(last_response, 'etag-2')

        # call should make both calls and print both responses
        expected = request.pretty_json(paging_response) + '\n' + \
                request.pretty_json(last_response) + '\n'
        self.assert_command_outputs(expected, '--path', '/', '--page-size', '2')

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
