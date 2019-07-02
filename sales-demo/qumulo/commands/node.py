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

import qumulo.lib.opts
import qumulo.rest.node as node

class NodeFullQuorum(qumulo.lib.opts.Subcommand):
    NAME = "node_full_quorum"
    DESCRIPTION = "Is the node in a full quorum?"

    @staticmethod
    def main(conninfo, credentials, _args):
        print node.node_full_quorum(conninfo, credentials)

class NodeSpecificQuorum(qumulo.lib.opts.Subcommand):
    NAME = "node_specific_quorum"
    DESCRIPTION = "Is the node in a specific quorum?"

    @staticmethod
    def options(parser):
        parser.add_argument(
            "--nodes", nargs="+", help="Expected nodes in quorum (uuids)",
            type=str)

    @staticmethod
    def main(conninfo, credentials, args):
        print node.node_specific_quorum(conninfo, credentials, args.nodes)
