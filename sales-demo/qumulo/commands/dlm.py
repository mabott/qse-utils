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

import qumulo.lib.opts
import qumulo.rest.dlm as dlm

class DumpAllLocksCommand(qumulo.lib.opts.Subcommand):
    NAME = "dlm_dump_locks"
    DESCRIPTION = "Dump DLM locks"

    @staticmethod
    def main(conninfo, credentials, _args):
        dump = dlm.dump_i_locks(conninfo, credentials)
        print dump[0]['value']
        dump = dlm.dump_c_locks(conninfo, credentials)
        print dump[0]['value']

class DumpLockStatsCommand(qumulo.lib.opts.Subcommand):
    NAME = "dlm_dump_stats"
    DESCRIPTION = "Dump DLM initiator stats"

    @staticmethod
    def main(conninfo, credentials, _args):
        dump = dlm.dump_lock_stats(conninfo, credentials)
        print dump

class CoordCountersCommand(qumulo.lib.opts.Subcommand):
    NAME = "dlm_coord_counters"
    DESCRIPTION = "Get DLM coordinator lock counters"

    @staticmethod
    def main(conninfo, credentials, _args):
        counters = dlm.coord_counters(conninfo, credentials)
        print counters

class InitiatorCountersCommand(qumulo.lib.opts.Subcommand):
    NAME = "dlm_initiator_counters"
    DESCRIPTION = "Get DLM initiator lock counters"

    @staticmethod
    def main(conninfo, credentials, _args):
        counters = dlm.initiator_counters(conninfo, credentials)
        print counters
