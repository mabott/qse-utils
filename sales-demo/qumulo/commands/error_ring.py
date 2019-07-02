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
import qumulo.rest.error_ring as error_ring

class DumpErrorRing(qumulo.lib.opts.Subcommand):
    NAME = "dump_error_ring"
    DESCRIPTION = "Dump error ring contents"

    @staticmethod
    def options(parser):
        parser.add_argument("-n", help="Number of entries to return", default=0)

    @staticmethod
    def main(conninfo, credentials, args):
        print('oldest->newest\n')
        print error_ring.dump_error_ring(conninfo, credentials, args.n)
