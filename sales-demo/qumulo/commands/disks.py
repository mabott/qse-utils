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
import qumulo.rest.disks as disks

class GetDisksStatus(qumulo.lib.opts.Subcommand):
    NAME = "disks_status_get"
    DESCRIPTION = "Get information about internal disk status"

    @staticmethod
    def main(conninfo, credentials, _args):
        print disks.disks_status_get(conninfo, credentials)

class GetDisksCounters(qumulo.lib.opts.Subcommand):
    NAME = "disks_counters_get"
    DESCRIPTION = "Return debug counters for disks"

    @staticmethod
    def main(conninfo, credentials, _args):
        print disks.disks_counters_get(conninfo, credentials)
