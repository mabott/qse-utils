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

import qumulo.lib.opts
import qumulo.rest.unconfigured_node_operations as node_operations

class UnconfiguredCommand(qumulo.lib.opts.Subcommand):
    NAME = "unconfigured"
    DESCRIPTION = "Is the node unconfigured?"

    @staticmethod
    def main(conninfo, credentials, _args):
        print node_operations.unconfigured(
            conninfo, credentials)

class ListUnconfiguredNodesCommand(qumulo.lib.opts.Subcommand):
    NAME = "unconfigured_nodes_list"
    DESCRIPTION = "Get the list of unconfigured nodes"

    @staticmethod
    def main(conninfo, credentials, _args):
        print node_operations.list_unconfigured_nodes(
            conninfo, credentials)

class CreateCluster(qumulo.lib.opts.Subcommand):
    NAME = "cluster_create"
    DESCRIPTION = "Creates a Qumulo Cluster"

    @staticmethod
    def options(parser):
        parser.add_argument("--cluster-name", help="Cluster Name",
                            required=True)
        parser.add_argument("--admin-password",
                            help="Administrator Pasword", required=True)
        parser.add_argument("--node-uuids", help="Cluster node uuid",
                            action="append", required=True)
        parser.add_argument("--require-full-quorum",
                            help="Disallow N-1 quorums", action="store_true",
                            default=None)

    @staticmethod
    def main(conninfo, credentials, args):
        extra_options = {}
        if (args.require_full_quorum is not None):
            extra_options['require_full_quorum'] = True

        print node_operations.create_cluster(
            conninfo, credentials, args.cluster_name, args.admin_password,
            args.node_uuids, extra_options)

class AddNode(qumulo.lib.opts.Subcommand):
    NAME = "add_nodes"
    DESCRIPTION = "Add unconfigured nodes to a Qumulo Cluster"

    @staticmethod
    def options(parser):
        parser.add_argument("--node-uuids",
                            help="Unconfigured node uuids to add",
                            action="append",
                            required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print node_operations.add_node(conninfo, credentials,
            args.node_uuids)
