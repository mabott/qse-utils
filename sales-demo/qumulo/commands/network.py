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
import qumulo.lib.util
import qumulo.rest.network as network

class ModifyClusterNetworkConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "network_conf_mod"
    DESCRIPTION = "Modify cluster-wide network config"

    @staticmethod
    def options(parser):
        parser.add_argument("--assigned-by", choices=[ 'DHCP', 'STATIC' ],
            help="Specify mechanism for IP configuration")
        parser.add_argument("--ip-ranges", action="append",
            help="(if STATIC) IP ranges, e.g. 10.1.1.20-21")
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--floating-ip-ranges", action="append",
            help="(if STATIC) Floating IP ranges, e.g. 10.1.1.20-21")
        group.add_argument("--clear-floating-ip-ranges",
            action="store_const", const=[], dest="floating_ip_ranges",
            help="(if STATIC) Remove all floating ip ranges")
        parser.add_argument("--netmask",
            help="(if STATIC) Netmask")
        parser.add_argument("--gateway",
            help="(if STATIC) Gateway address")
        parser.add_argument("--dns-servers", action="append",
            help="(if STATIC) DNS server")
        parser.add_argument("--dns-search-domains", action="append",
            help="(if STATIC) DNS search domain")

    @staticmethod
    def main(conninfo, credentials, args):
        if (args.assigned_by == 'DHCP'
            and any([args.dns_servers, args.dns_search_domains,
                     args.ip_ranges, args.gateway, args.netmask])):
            raise ValueError(
                "DHCP configuration conflicts with static configuration")

        attributes = { key: getattr(args, key) for key in network.FIELDS
                if getattr(args, key) is not None }

        if not attributes:
            raise ValueError("One or more options must be specified")

        print network.modify_cluster_network_config(conninfo, credentials,
                **attributes)

class MonitorNetworkCommand(qumulo.lib.opts.Subcommand):
    NAME = "network_poll"
    DESCRIPTION = "Poll network changes"

    @staticmethod
    def options(parser):
        parser.add_argument("--node-id", help="Node ID")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.node_id is not None:
            print network.get_network_status(
                conninfo, credentials, args.node_id)
        else:
            print network.list_network_status(conninfo, credentials)

class GetClusterNetworkConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "network_conf_get"
    DESCRIPTION = "Get cluster-wide network config"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print network.get_cluster_network_config(conninfo, credentials)

class GetStaticIpAllocationCommand(qumulo.lib.opts.Subcommand):
    NAME = "static_ip_allocation"
    DESCRIPTION = "Get cluster-wide static IP allocation"

    @staticmethod
    def options(parser):
        parser.add_argument("--try-ranges",
            help="Specify ip range list to try "
                 "(e.g. '1.1.1.10-12,10.20.5.0/24'")
        parser.add_argument("--try-netmask",
            help="Specify netmask to apply when using --try-range option")
        parser.add_argument("--try-floating-ranges",
            help="Specify floating ip range list to try "
                 "(e.g. '1.1.1.10-12,10.20.5.0/24'")

    @staticmethod
    def main(conninfo, credentials, args):
        print network.get_static_ip_allocation(
            conninfo, credentials,
            args.try_ranges, args.try_netmask, args.try_floating_ranges)

class GetFloatingIpAllocationCommand(qumulo.lib.opts.Subcommand):
    NAME = "floating_ip_allocation"
    DESCRIPTION = "Get cluster-wide floating IP allocation"

    @staticmethod
    def main(conninfo, credentials, _args):
        print network.get_floating_ip_allocation(conninfo, credentials)
