#!/usr/bin/env python
# Copyright (c) 2014 Qumulo, Inc.
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

import mock
import unittest

import qumulo.commands.shutdown as shutdown

class CommandTest(unittest.TestCase):
    def setUp(self):
        self.conninfo = mock.Mock()
        self.credentials = mock.Mock()

        self.args = mock.Mock()
        setattr(self.args, 'force', False)

    def test_ask(self):
        with mock.patch('__builtin__.raw_input') as input_patch:
            input_patch.return_value = 'no'
            self.assertFalse(shutdown.ask('command', 'target'))

            input_patch.return_value = 'NO'
            self.assertFalse(shutdown.ask('command', 'target'))

            input_patch.return_value = 'KEK'
            with self.assertRaisesRegexp(ValueError,
                                            "Please enter 'yes' or 'no'"):
                shutdown.ask('command', 'target')

            input_patch.return_value = 'yes'
            self.assertTrue(shutdown.ask('command', 'target'))

    def shutdown_test(self, command_class, rest_function):
        with mock.patch(rest_function) as rest_patch:
            with mock.patch('qumulo.commands.shutdown.ask') as ask_patch:
                ask_patch.return_value = False
                command_class.main(self.conninfo, self.credentials, self.args)
                self.assertEqual(rest_patch.call_count, 0)

                self.args.force = True
                command_class.main(self.conninfo, self.credentials, self.args)
                self.assertEqual(rest_patch.call_count, 1)

                ask_patch.return_value = True
                command_class.main(self.conninfo, self.credentials, self.args)
                self.assertEqual(rest_patch.call_count, 2)

                self.args.force = False
                command_class.main(self.conninfo, self.credentials, self.args)
                self.assertEqual(rest_patch.call_count, 3)

    def test_restart(self):
        self.shutdown_test(shutdown.RestartCommand,
                           'qumulo.rest.shutdown.restart')

    def test_restart_cluster(self):
        self.shutdown_test(shutdown.RestartClusterCommand,
                           'qumulo.rest.shutdown.restart_cluster')

    def test_halt(self):
        self.shutdown_test(shutdown.HaltCommand,
                           'qumulo.rest.shutdown.halt')

    def test_halt_cluster(self):
        self.shutdown_test(shutdown.HaltClusterCommand,
                           'qumulo.rest.shutdown.halt_cluster')

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
