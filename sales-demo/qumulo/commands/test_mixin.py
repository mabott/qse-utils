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

import mock
import qumulo.lib.request as request
import qumulo.lib.opts
import argparse
import StringIO

class CommandTest(object):
    'Base class for tests of commands.'

    def setUp(self, class_, name, *patches):
        '''Set up a CommandTest.

        This should be called by subclasses' own setUp method, which will be
        called before every test.

        The first three arguments specify the class under test, the name of the
        command, and whether it requires credentials.

        The remaining arguments are strings that specify the name of extern
        symbols that should be patched with mocks for every test. Those mocks
        are attached to the self.mock object. For example:
            setUp(MyCommand, 'my_command', True,
                'qumulo.rest.my.something_rest', 'qumulo.rest.my.other_rest')
        will result in 'something_rest' and 'other_rest' being patched during
        all the tests, with the patched versions being mocks accessible as
        self.mock.something_rest and self.mock.other_rest.
        '''
        self.class_ = class_
        self.name = name
        self.conninfo = mock.Mock()
        self.credentials = mock.Mock()
        self.request_error = request.RequestError(400, "test", None)

        # Set up mocks for all of the patches.
        self.mock = mock.Mock()
        for patch in patches:
            patcher = mock.patch(patch)
            request_mock = patcher.start()
            self.addCleanup(patcher.stop)
            self.mock.attach_mock(request_mock, patch.split('.')[-1])

    def run_command(self, argv):
        'Run the command with the given arguments.'
        argv = [ self.name ] + list(argv)
        args = qumulo.lib.opts.parse_options(argparse.ArgumentParser(), argv)
        args.request.main(self.conninfo, self.credentials, args)

    def assert_command_raises(self, exception_class, *args):
        'Run the command and assert it raises the given exception.'
        self.assertRaises(exception_class, self.run_command, args)

    def assert_exit_regexp(self, regexp, *args):
        '''
        Run the command and assert it exits and prints something to standard
        error that matches the given regexp.
        '''

        with mock.patch('sys.stderr', new_callable=StringIO.StringIO) as \
                mock_stderr:
            self.assertRaises(SystemExit, self.run_command, args)
        self.assertRegexpMatches(mock_stderr.getvalue(), regexp)

    def assert_missing_argument(self, missing, *args):
        'Assert the command fails because an argument is missing.'
        self.assert_exit_regexp('error: argument %s is required' % missing,
            *args)

    def assert_missing_value(self, missing, *rest):
        'Assert the command fails because an argument is missing a value.'
        self.assert_exit_regexp('error: argument %s: expected one argument' %
            missing, missing, *rest)

    def assert_bad_int_value(self, arg, bad_value, *rest):
        '''Assert the command fails because an argument has an invalid int
        value.'''
        self.assert_exit_regexp('error: argument %s: invalid int value' % arg,
            arg, bad_value, *rest)

    def assert_extra_argument(self, *args):
        '''Assert the command fails because extra arguments are given after the
        options.'''
        self.assert_exit_regexp('error: unrecognized arguments', *args)

    def assertEqual(self, output, expected):
        if output != expected:
            msg = "OUTPUT:\n" + output + "\n!= EXPECTED:\n" + expected + "\n"
            raise AssertionError(msg)

    def assert_command_outputs(self, expected, *args):
        '''Assert the command runs successfully and prints the expected output
        to standard output.

        If expected is a string, then it must match standard output exactly.
        Otherwise, it is assumed to be a json object and standard output is
        expected to match pretty_json(expected).
        '''
        with mock.patch('sys.stdout', new_callable=StringIO.StringIO) as \
                mock_stdout:
            self.run_command(args)
        if not isinstance(expected, basestring):
            expected = request.pretty_json(expected) + '\n'
        self.assertEqual(mock_stdout.getvalue(), expected)

    def assert_call_list(self, *calls):
        'Assert that exactly the given calls were made, in order.'
        calls = list(calls)
        self.mock.assert_has_calls(calls)
        self.assertEqual(len(self.mock.mock_calls), len(calls))

    def test_has_name_and_description(self):
        '''Test that the command class has the appropriate NAME and DESCRIPTION
        class variables.'''
        self.assertEqual(self.class_.NAME, self.name)
        self.assertIsNotNone(self.class_.DESCRIPTION)

