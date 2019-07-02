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

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.lib.log as log
import qumulo.rest.auth as auth
from qumulo.lib.request import NEED_LOGIN_MESSAGE

class LoginCommand(qumulo.lib.opts.Subcommand):
    NAME = "login"
    DESCRIPTION = "Log in to qfsd to get REST credentials"

    @staticmethod
    def options(parser):
        parser.add_argument("-u", "--username", type=str, default=None,
                            required=True, help="User name")
        parser.add_argument("-p", "--password", type=str, default=None,
                            help="Password (insecure, visible via ps)")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.password is None:
            password = qumulo.lib.opts.read_password(prompt='Password: ')
        else:
            password = args.password

        login_resp, _ = auth.login(conninfo, credentials, args.username,
            password)
        qumulo.lib.auth.set_credentials(login_resp, args.credentials_store)

class LogoutCommand(qumulo.lib.opts.Subcommand):
    NAME = "logout"
    DESCRIPTION = "Remove qfsd REST credentials"

    @staticmethod
    def options(parser):
        parser.add_argument("-k", "--keep", action="store_true", default=False,
                            help="Keep local credentials cache")

    @staticmethod
    def main(_, credentials, args):
        # Don't bother the server for logout with no credentials
        if not credentials:
            log.fatal("Error 401: unknown: " + NEED_LOGIN_MESSAGE)

        # Remove credentials
        if not args.keep:
            log.info("Removing REST credentials")
            qumulo.lib.auth.remove_credentials_store(args.credentials_store)
        else:
            log.info("Leaving local REST credentials cache")

        # Print nothing on success

class WhoAmICommand(qumulo.lib.opts.Subcommand):
    NAME = "who_am_i"
    DESCRIPTION = "Get information on the current user"

    @staticmethod
    def main(conninfo, credentials, _args):
        print auth.who_am_i(conninfo, credentials)
