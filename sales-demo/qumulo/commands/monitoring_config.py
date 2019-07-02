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

import os

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.monitoring_config as monitoring_config

class GetMonitoringConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "monitoring_conf"
    DESCRIPTION = "Get monitoring configuration."

    @staticmethod
    def main(conninfo, credentials, _args):
        print monitoring_config.get_config(conninfo, credentials)

class SetMonitoringConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "set_monitoring_conf"
    DESCRIPTION = "Update monitoring configuration."

    @staticmethod
    def options(parser):
        parser.add_argument("--enabled", action='store_true', default=None,
            help="Enable monitoring service.")
        parser.add_argument("--disabled", dest='enabled', action='store_false',
            help="Disable monitoring service.")
        parser.add_argument("--vpn-enabled", action='store_true', default=None,
            help="Enable support VPN.")
        parser.add_argument("--vpn-disabled", dest='vpn_enabled',
                action='store_false', help="Disable support VPN.")
        parser.add_argument("--mq-host",
            help="Specify MQ host name or IP.")
        parser.add_argument("--mq-port", type=int,
            help="Optional MQ service port.")
        parser.add_argument("--s3-proxy-host",
            help="Optional S3 proxy host.")
        parser.add_argument("--s3-proxy-port", type=int,
            help="Optional S3 proxy port.")
        parser.add_argument("--period", type=int,
            help="Monitoring poll interval in seconds.")
        parser.add_argument("--vpn-host",
            help="Support VPN host name or IP.")

    @staticmethod
    def main(conninfo, credentials, args):
        config = {}

        for field in ['enabled', 'mq_host', 'mq_port',
                's3_proxy_host', 's3_proxy_port', 'period',
                'vpn_host', 'vpn_enabled']:
            value = getattr(args, field)
            if value is not None:
                config[field] = value

        if not config:
            raise ValueError('No options supplied')

        print monitoring_config.set_config(conninfo, credentials, **config)

class GetVpnKeysCommand(qumulo.lib.opts.Subcommand):
    NAME = "get_vpn_keys"
    DESCRIPTION = "Get VPN keys stored in the cluster."

    @staticmethod
    def main(conninfo, credentials, _args):
        print monitoring_config.get_vpn_keys(conninfo, credentials)

class InstallVpnKeysCommand(qumulo.lib.opts.Subcommand):
    NAME = "install_vpn_keys"
    DESCRIPTION = "Install VPN keys."

    @staticmethod
    def options(parser):
        parser.add_argument("directory",
            help="Directory with mqvpn-client.crt, mqvpn-client.key, "
                 "and qumulo-ca.crt files.")

    @staticmethod
    def main(conninfo, credentials, args):
        directory = os.path.abspath(args.directory)

        def load_file(filename):
            with open(os.path.join(directory, filename)) as f:
                return f.read()

        vpn_keys = {
            'mqvpn_client_crt': load_file('mqvpn-client.crt'),
            'mqvpn_client_key': load_file('mqvpn-client.key'),
            'qumulo_ca_crt':    load_file('qumulo-ca.crt')
        }

        monitoring_config.install_vpn_keys(conninfo, credentials, vpn_keys)
