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

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.ad as ad

class ListAdCommand(qumulo.lib.opts.Subcommand):
    NAME = "ad_list"
    DESCRIPTION = "List Active Directory configuration"

    @staticmethod
    def main(conninfo, credentials, _args):
        print ad.list_ad(conninfo, credentials)

class PollAdCommand(qumulo.lib.opts.Subcommand):
    NAME = "ad_poll"
    DESCRIPTION = "Poll Active Directory configuration"

    @staticmethod
    def main(conninfo, credentials, _args):
        print ad.poll_ad(conninfo, credentials)

def add_ad_options(parser, creds_required):
    parser.add_argument("-d", "--domain", type=str, default=None, required=True,
                        help="Fully-qualified name of Domain Controller")
    parser.add_argument("-u", "--username", type=str, default=None,
                        help="Username on Domain Controller",
                        required=creds_required)
    parser.add_argument("-p", "--password", type=str, default=None,
                        help="Password on Domain Controller",
                        required=creds_required)

class JoinAdCommand(qumulo.lib.opts.Subcommand):
    NAME = "ad_join"
    DESCRIPTION = "Join an Active Directory Domain"

    @staticmethod
    def options(parser):
        add_ad_options(parser, True)
        parser.add_argument("--domain-netbios", type=str, required=False,
            help="NetBIOS name of the domain. By default, the first part of "
                 "the domain name is used.")
        parser.add_argument("-o", "--ou", type=str, default="", required=False,
            help="Organizational Unit to join to")

    @staticmethod
    def main(conninfo, credentials, args):
        print ad.join_ad(
            conninfo, credentials, args.domain, args.username, args.password,
            args.ou, domain_netbios=args.domain_netbios)

class LeaveAdCommand(qumulo.lib.opts.Subcommand):
    NAME = "ad_leave"
    DESCRIPTION = "Leave an Active Directory Domain"

    @staticmethod
    def options(parser):
        add_ad_options(parser, False)

    @staticmethod
    def main(conninfo, credentials, args):
        print ad.leave_ad(conninfo, credentials, args.domain,
                                  args.username, args.password)

class CancelAdCommand(qumulo.lib.opts.Subcommand):
    NAME = "ad_cancel"
    DESCRIPTION = "Cancel current AD join/leave operation and clear errors"

    @staticmethod
    def main(conninfo, credentials, _args):
        print ad.cancel_ad(conninfo, credentials)

class SetAdMachineAccount(qumulo.lib.opts.Subcommand):
    NAME = "ad_set_machine_account"
    DESCRIPTION = "Set the machine account used for AD"

    @staticmethod
    def options(parser):
        parser.add_argument("-d", "--domain", type=str, default=None,
            help="Fully-qualified name of Domain Controller",
            required=True)
        parser.add_argument("-u", "--username", type=str, default=None,
            help="Machine user name",
            required=True)
        parser.add_argument("-p", "--password", type=str, default=None,
            help="Machine user password",
            required=True)
        parser.add_argument("-s", "--salt", type=str, default=None,
            help="Machine account salt (principal)",
            required=True)
        parser.add_argument("-i", "--sid", type=str, default=None,
            help="Machine account sid",
            required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print ad.set_ad_machine_account(
            conninfo, credentials, args.domain, args.username,
            args.password, args.salt, args.sid)
