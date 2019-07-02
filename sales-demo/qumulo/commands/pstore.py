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

import qumulo.lib.auth
import qumulo.lib.opts
import qumulo.rest.pstore as pstore

class GetPstore(qumulo.lib.opts.Subcommand):
    NAME = "pstore_get"
    DESCRIPTION = "Get information on pstores"

    @staticmethod
    def options(parser):
        parser.add_argument(
            "--pstore", help="Get information on a specific pstore",
            required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        print pstore.pstore_get(conninfo, credentials, args.pstore)

class PostPstoreFill(qumulo.lib.opts.Subcommand):
    NAME = "pstore_fill"
    DESCRIPTION = "Fill a pstore"

    @staticmethod
    def options(parser):
        parser.add_argument("--pstore", help="Pstore ID to fill.")
        parser.add_argument(
            "--unexpired_percentage",
            "--percentage",
            help="Fill pstore to percentage with normal data (default: 0).",
            type=int, default=0)
        parser.add_argument(
            "--expired_percentage",
            help="Fill percentage with expired hybrid data (default: 0).",
            type=int, default=0)
        parser.add_argument(
            "--fast",
            help="Fills a pstore much more rapidly by bypassing the "
                 "transaction system altogether. The data in the pstore "
                 "mirrors will not be consistent, so calls to fs_verify will "
                 "fail. This method should only be used for test purposes in "
                 "controlled environments",
            action="store_true",
            required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        pstore.pstore_fill_post(
            conninfo, credentials, args.pstore,
            args.unexpired_percentage, args.expired_percentage, args.fast)

class PostPstorePushLayer(qumulo.lib.opts.Subcommand):
    NAME = "pstore_push_layer"
    DESCRIPTION = "Push a layer on a pstore"

    @staticmethod
    def options(parser):
        parser.add_argument("--pstore", help="Pstore ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        pstore.pstore_push_layer_post(
            conninfo, credentials, args.pstore)

