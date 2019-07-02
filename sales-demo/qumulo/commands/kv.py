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
import qumulo.rest.kv as kv

class GetKvCommand(qumulo.lib.opts.Subcommand):
    NAME = "kv_get"
    DESCRIPTION = "Get a value from the key-value store"

    @staticmethod
    def options(parser):
        parser.add_argument("--key", help="Key of value to retrieve",
            required=True)
        parser.add_argument("--uid", type=int, help="User ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print kv.get(conninfo, credentials, args.key, args.uid)

class SetKvCommand(qumulo.lib.opts.Subcommand):
    NAME = "kv_set"
    DESCRIPTION = "Set a value in the key-value store"

    @staticmethod
    def options(parser):
        parser.add_argument("--key", help="Key of value to set", required=True)
        parser.add_argument("--value", help="Value to set", required=True)
        parser.add_argument("--uid", type=int, help="User ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print kv.put(conninfo, credentials, args.key, args.value, args.uid)

class DeleteKvCommand(qumulo.lib.opts.Subcommand):
    NAME = "kv_delete"
    DESCRIPTION = "Delete a key-value pair in the key-value store"

    @staticmethod
    def options(parser):
        parser.add_argument("--key", help="Key to delete", required=True)
        parser.add_argument("--uid", type=int, help="User ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print kv.delete(conninfo, credentials, args.key, args.uid)
