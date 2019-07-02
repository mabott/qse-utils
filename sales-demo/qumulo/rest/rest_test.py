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

class RestTest(object):
    'Base class for tests of rest requests.'

    def setUp(self, func, http_method):
        '''Set up a RestTest.

        This should be called by subclasses' own setUp method, which will be
        called before every test.

        Func should be the rest request function (such as
        qumulo.rest.fs.get_attr_request) that you want to test.

        The http_method argument should be the expected method, one of "GET",
        "PUT", "POST" or "DELETE".
        '''

        self.func = func
        self.http_method = http_method

        # Mock these to make sure they are passed through
        self.conninfo = mock.Mock()
        self.credentials = mock.Mock()

        # Set up mock for rest_request
        request_patcher = mock.patch('qumulo.lib.request.rest_request')
        self.request_mock = request_patcher.start()
        self.addCleanup(request_patcher.stop)

    def run_command(self, *args, **kwargs):
        'Run the command with the given arguments.'
        self.func(self.conninfo, self.credentials, *args, **kwargs)

    def assertCalledWith(self, exp_uri, **kwargs):
        '''Assert the command was called with an expected URI and specific
        keyword arguments. Use mock.Mock() for arguments that should be passed
        through. '''
        self.request_mock.assert_called_with(self.conninfo, self.credentials,
            self.http_method, exp_uri, **kwargs)

    def assert_request_raises(self, exception_class, *args, **kwargs):
        'Run the command and assert it raises the given exception.'
        self.assertRaises(exception_class, self.run_command, *args, **kwargs)
