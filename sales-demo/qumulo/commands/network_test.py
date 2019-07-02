#!/usr/bin/env python
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

import mock
import unittest

import qumulo.commands.network as network
import qumulo.rest.network as network_rest

class CommandTest(unittest.TestCase):
    def setUp(self):
        self.conninfo = mock.Mock()
        self.credentials = mock.Mock()

        self.args = mock.Mock()
        setattr(self.args, 'assigned_by', 'DHCP')

        for arg in ['ip_ranges', 'netmask', 'gateway', 'dns_servers',
                    'dns_search_domains', 'floating_ip_ranges']:
            setattr(self.args, arg, None)

    def test_modify(self):
        network_rest.modify_cluster_network_config = mock.Mock()

        network.ModifyClusterNetworkConfigCommand.main(
            self.conninfo, self.credentials, self.args)
        self.assertEqual(
            network_rest.modify_cluster_network_config.call_count, 1)

        self.args.dns_search_domains = ['qumulo.com']
        with self.assertRaisesRegexp(
            ValueError,
            "DHCP configuration conflicts with static configuration"):
            network.ModifyClusterNetworkConfigCommand.main(
                self.conninfo, self.credentials, self.args)

        self.args.assigned_by = 'STATIC'
        network.ModifyClusterNetworkConfigCommand.main(
            self.conninfo, self.credentials, self.args)
        self.assertEqual(
            network_rest.modify_cluster_network_config.call_count, 2)

    def test_modify_empty(self):
        self.args.assigned_by = None
        with self.assertRaisesRegexp(ValueError, "options must be specified"):
            network.ModifyClusterNetworkConfigCommand.main(
                self.conninfo, self.credentials, self.args)

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
