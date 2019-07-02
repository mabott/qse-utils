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
import qumulo.lib.request as request
import qumulo.commands.auth
from qumulo.commands.test_mixin import CommandTest

class MoUserCommandTest(unittest.TestCase, CommandTest):
    def setUp(self):
        CommandTest.setUp(self, qumulo.commands.auth.ModUserCommand,
            'auth_mod_user',
            'qumulo.rest.users.list_user',
            'qumulo.rest.users.list_groups_for_user',
            'qumulo.rest.users.modify_user',
            )

    def mock_call(self, name, *args):
        method = getattr(mock.call, name)
        return method(self.conninfo, self.credentials, *args)

    def test_name_and_primary_group(self):
        '''
        The whole point of this test is to make sure that we are
        using etag when modifying a user object.
        '''

        attributes_1 = {
            'id':             '10',
            'name':           'billy-1',
            'primary_group':  '20',
            'sid':            'billy-sid-1',
            'uid':            'billy-uid-1',
        }

        attributes_2 = {
            'id':             '10',
            'name':           'billy-2',
            'primary_group':  '21',
            'sid':            'billy-sid-1',
            'uid':            'billy-uid-1',
        }

        expected_stdout = '\n'.join([
            '{',
            '    "id": "10", ',
            '    "name": "billy-2", ',
            '    "primary_group": "21", ',
            '    "sid": "billy-sid-1", ',
            '    "uid": "billy-uid-1"',
            '}',
            'User 10 is a member of following groups: [',
            '    "unused"',
            ']',
            '',
            ])

        # Mock rest methods
        self.mock.list_user.side_effect = [
            request.RestResponse(attributes_1, 'etag-1'),
            request.RestResponse(attributes_2, 'etag-2')]

        self.mock.list_groups_for_user.return_value = \
            request.RestResponse(['unused'], None)

        self.mock.modify_user.return_value = \
            request.RestResponse(attributes_2, 'etag-2')

        # Execute command module
        self.assert_command_outputs(expected_stdout,
            '--id', '10', '--name', 'billy-2', '--primary-group', '21')

        self.assert_call_list(
            self.mock_call('list_user', 10),
            self.mock_call('modify_user', 10,
                'billy-2', '21', 'billy-uid-1', 'etag-1'),
            self.mock_call('list_user', 10),
            self.mock_call('list_groups_for_user', 10))

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
