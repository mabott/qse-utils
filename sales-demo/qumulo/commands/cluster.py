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
import qumulo.lib.util
import qumulo.rest.cluster as cluster
import qumulo.rest.disrupt as disrupt

class ListNodesCommand(qumulo.lib.opts.Subcommand):
    NAME = "nodes_list"
    DESCRIPTION = "List nodes"

    @staticmethod
    def options(parser):
        parser.add_argument("--node", help="Node ID")

    @staticmethod
    def main(conninfo, credentials, _args):
        if _args.node is not None:
            print cluster.list_node(conninfo, credentials, _args.node)
        else:
            print cluster.list_nodes(conninfo, credentials)

class GetClusterConfCommand(qumulo.lib.opts.Subcommand):
    NAME = "cluster_conf"
    DESCRIPTION = "Get the cluster config"

    @staticmethod
    def main(conninfo, credentials, _args):
        print cluster.get_cluster_conf(conninfo, credentials)

class SetClusterConfCommand(qumulo.lib.opts.Subcommand):
    NAME = "set_cluster_conf"
    DESCRIPTION = "Set the cluster config"

    @staticmethod
    def options(parser):
        parser.add_argument("--cluster-name", help="Cluster Name",
                            required=True)

    @staticmethod
    def main(conninfo, credentials, _args):
        print cluster.put_cluster_conf(conninfo, credentials,
            _args.cluster_name)

class GetClusterSlotStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = "cluster_slots"
    DESCRIPTION = "Get the cluster disk slots status"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot", help="Slot ID")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.slot is not None:
            print cluster.get_cluster_slot_status(
                conninfo, credentials, args.slot)
        else:
            print cluster.get_cluster_slots_status(
                conninfo, credentials)

class GetRestriperStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = "restriper_status"
    DESCRIPTION = "Get restriper and data protection status"

    @staticmethod
    def main(conninfo, credentials, _args):
        print cluster.get_restriper_status(conninfo, credentials)

class RestriperDisableCommand(qumulo.lib.opts.Subcommand):
    NAME = "restriper_disable"
    DESCRIPTION = "Make the restriper stop before reprotect begins"

    @staticmethod
    def main(conninfo, credentials, _args):
        cluster.restriper_disable(conninfo, credentials, True)

class RestriperEnableCommand(qumulo.lib.opts.Subcommand):
    NAME = "restriper_enable"
    DESCRIPTION = "Allows the restriper to complete on next quorum. " \
        "And bounces quorum unless the do-not-bounce-quorum flag is set."

    @staticmethod
    def options(parser):
        parser.add_argument("--do-not-bounce-quorum", action='store_true')

    @staticmethod
    def main(conninfo, credentials, args):
        cluster.restriper_disable(conninfo, credentials, False)

        if not args.do_not_bounce_quorum:
            # If we have not encountered an error, then make quorum bounce
            disrupt.rpc_glitch(conninfo, credentials, "2")

class GetClusterRPCStatsCommand(qumulo.lib.opts.Subcommand):
    NAME = "cluster_rpc_stats"
    DESCRIPTION = "Return cluster RPC stats for debugging purposes."

    @staticmethod
    def main(conninfo, credentials, _args):
        print cluster.get_rpc_stats(conninfo, credentials)
