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
import qumulo.rest.debug_file as debug_file

class QuickFileCommand(qumulo.lib.opts.Subcommand):
    NAME = "repeat_write"
    DESCRIPTION = "Create a file quickly of a certain size filled with the \
        given byte"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", type=str, required=True,
                            help="Path to file")
        parser.add_argument("--size", type=int, required=True,
                            help="Size of the file")
        parser.add_argument("--byte", type=int, required=True,
                            help="The byte to write to the file repeatedly")
        parser.add_argument("--transaction-size", type=int, required=False,
                            help="Transaction size to write with")

    @staticmethod
    def main(conninfo, credentials, args):
        print debug_file.repeat_write(conninfo, credentials, args.path,
            args.size, args.byte, args.transaction_size)
