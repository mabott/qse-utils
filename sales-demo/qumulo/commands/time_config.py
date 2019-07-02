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

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.time_config as time_config

class GetTimeCommand(qumulo.lib.opts.Subcommand):
    NAME = "time_get"
    DESCRIPTION = "Get time configuration."

    @staticmethod
    def main(conninfo, credentials, _args):
        print time_config.get_time(conninfo, credentials)

class SetTimeCommand(qumulo.lib.opts.Subcommand):
    NAME = "time_set"
    DESCRIPTION = "Set time configuration."

    @staticmethod
    def options(parser):
        parser.add_argument("--set-use-ad", required=False, action='store_true',
                default=None, help="Use Active Directory controller for NTP.",
                dest='use_ad')
        parser.add_argument("--unset-use-ad", required=False,
                action='store_false', default=None, help="Don't use Active\
                Directory controller for NTP.", dest='use_ad')
        parser.add_argument("--ntp-servers", type=str, default=None,
            help="Set of NTP servers specified as comma delimited list.")

    @staticmethod
    def main(conninfo, credentials, args):
        ntp_servers = None
        if args.ntp_servers:
            ntp_servers = [x.strip() for x in args.ntp_servers.split(',')]

        print time_config.set_time(conninfo, credentials, args.use_ad,
                                           ntp_servers)

class GetTimeStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = "time_status"
    DESCRIPTION = "Get time configuration status."

    @staticmethod
    def main(conninfo, credentials, _arg):
        print time_config.get_time_status(conninfo, credentials)
