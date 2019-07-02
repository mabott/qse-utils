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

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.rest.quiesce as quiesce

class DeferredGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "quiesce_deferred"
    DESCRIPTION = "Wait until the deferred worker has finished"

    @staticmethod
    def main(conninfo, credentials, _args):
        quiesce.deferred(conninfo, credentials)

class HostConfigGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "quiesce_host_config"
    DESCRIPTION = "Wait until host config has no unapplied updates"

    @staticmethod
    def main(conninfo, credentials, _args):
        quiesce.host_config(conninfo, credentials)

class PstoreAllocationCacheGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "quiesce_pstore_allocation_cache"
    DESCRIPTION = "Wait for most up to date pstore allocation information"

    @staticmethod
    def main(conninfo, credentials, _args):
        quiesce.pstore_allocation_cache(conninfo, credentials)
