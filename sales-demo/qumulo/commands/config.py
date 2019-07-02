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

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.rest.config as config

class ClusterConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "cluster_config_get"
    DESCRIPTION = "Returns detailed information about cluster config"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print config.cluster_config_get(conninfo, credentials)

class SystemConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "system_config_get"
    DESCRIPTION = "Returns detailed information about the system config " + \
        "on this specific node"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print config.system_config_get(conninfo, credentials)
