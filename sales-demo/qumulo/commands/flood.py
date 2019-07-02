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
import qumulo.rest.flood as flood

class FloodRpcPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "flood_rpc_start"
    DESCRIPTION = "Run a flood of RPC against target node in background"

    @staticmethod
    def options(parser):
        parser.add_argument("--remote-id", help="Remote Node ID", required=True)
        parser.add_argument("--count", help="Number of RPCs", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print flood.start_rpc_flood(
            conninfo, credentials, args.remote_id, args.count)

class FloodRpcGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "flood_rpc_status"
    DESCRIPTION = "Get status of RPC flood tasks"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print flood.get_flood_status(conninfo, credentials)
