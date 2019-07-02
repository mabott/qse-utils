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
import qumulo.rest.bstores as bstores

class GetBstoresSummary(qumulo.lib.opts.Subcommand):
    NAME = "bstores_summary_get"
    DESCRIPTION = "Get summary information about internal bstore status"

    @staticmethod
    def main(conninfo, credentials, _args):
        print bstores.bstores_summary_get(conninfo, credentials)

class GetBstoresStatus(qumulo.lib.opts.Subcommand):
    NAME = "bstores_status_get"
    DESCRIPTION = "Get specific information about internal bstore status"

    @staticmethod
    def main(conninfo, credentials, _args):
        print bstores.bstores_status_get(conninfo, credentials)

class BstoresEmptyAllWals(qumulo.lib.opts.Subcommand):
    NAME = "bstores_empty_all_wals"
    DESCRIPTION = "Empty all bstore WALs"

    @staticmethod
    def main(conninfo, credentials, _args):
        print bstores.bstores_empty_all_wals_post(conninfo, credentials)
