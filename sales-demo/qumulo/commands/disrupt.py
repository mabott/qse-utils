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
import qumulo.rest.disrupt as disrupt

class PanicPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "disrupt_panic"
    DESCRIPTION = "Force a node to immediately panic"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print disrupt.panic(conninfo, credentials)

class RpcGlitchPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "disrupt_rpc_glitch"
    DESCRIPTION = "Force a node to lose RPC connection to another node"

    @staticmethod
    def options(parser):
        parser.add_argument("--remote-id", help="Remote Node ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print disrupt.rpc_glitch(conninfo, credentials, args.remote_id)

class RpcDisconnectPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "disrupt_rpc_disconnect"
    DESCRIPTION = "Force a node to stay disconnected from another node"

    @staticmethod
    def options(parser):
        parser.add_argument("--remote-id", help="Remote Node ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print disrupt.rpc_disconnect(
            conninfo, credentials, args.remote_id)

class RpcReconnectPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "disrupt_rpc_reconnect"
    DESCRIPTION = "Allow a node to reconnect to another node"

    @staticmethod
    def options(parser):
        parser.add_argument("--remote-id", help="Remote Node ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print disrupt.rpc_reconnect(
            conninfo, credentials, args.remote_id)

class SleepPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "disrupt_sleep"
    DESCRIPTION = "Make a node sleep for a duration"

    @staticmethod
    def options(parser):
        parser.add_argument("--seconds", help="Time to Sleep", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print disrupt.sleep(conninfo, credentials, args.seconds)
