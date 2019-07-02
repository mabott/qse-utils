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
import qumulo.rest.inspect as inspect

import sys

def string_response_to_string(string_response):
    return string_response[0]['value']

class InspectSuperblockCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_superblock"
    DESCRIPTION = "Inspect the contents of the superblock"

    @staticmethod
    def options(parser):
        parser.add_argument("-x", "--hex", dest="use_hex", default=False,
            action="store_true", help="Dump the contents as hex",
            required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        response = inspect.superblock(conninfo, credentials,
            args.use_hex)

        print string_response_to_string(response)

class InspectMetatreeCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_metatree"
    DESCRIPTION = "Inspect the metatree"

    @staticmethod
    def options(parser):
        parser.add_argument("--inode", type=int,
            help="Specify a particular inode", required=True)

        parser.add_argument("--begin-offset", type=int, default=None,
            help="Begin offset to start dumping", required=False)

        parser.add_argument("--end-offset", type=int, default=None,
            help="End offset to finish dumping", required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        response = inspect.metatree(conninfo, credentials, args.inode,
            args.begin_offset, args.end_offset)

        print string_response_to_string(response)

class InspectDirectoryCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_directory"
    DESCRIPTION = "Inspect the directory"

    @staticmethod
    def options(parser):
        parser.add_argument("--inode", type=int,
            help="Specify a particular inode", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        response = inspect.directory(conninfo, credentials, args.inode)

        print string_response_to_string(response)

class InspectInodeCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_inode"
    DESCRIPTION = "Inspect an inode"

    @staticmethod
    def options(parser):
        parser.add_argument("-x", "--hex", dest="use_hex", default=False,
            action="store_true", help="Dump the contents as hex",
            required=False)

        parser.add_argument("-a", "--all-attrs", default=False,
            action="store_true", help="Print all inode attributes",
            required=False)

        parser.add_argument("--begin-inode", type=int, default=None,
            help="Begining inode", required=False)

        parser.add_argument("--end-inode", type=int, default=None,
            help="Ending inode", required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        response = inspect.inode(conninfo, credentials, args.use_hex,
            args.all_attrs, args.begin_inode, args.end_inode)

        print string_response_to_string(response)

class InspectVerifyPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "verify"
    DESCRIPTION = "Start a job to verify the consistency of the filesystem"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print string_response_to_string(inspect.verify(conninfo,
            credentials))

class InspectVerifyOfflinePostCommand(qumulo.lib.opts.Subcommand):
    NAME = "verify_offline"
    DESCRIPTION = "Verify the integrity of the filesystem, WARNING: This api " \
        "is unsafe, make sure there is no load on the system before calling."

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print "Verifying filesystem..."
        inspect.verify_offline(conninfo, credentials)
        print "Filesystem ok."

class InspectVerifyStatusCommand(qumulo.lib.opts.Subcommand):
    NAME = "verify_status"
    DESCRIPTION = "Check the status of the last verify job ran"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        response, _etag = inspect.verify_status(conninfo, credentials)
        status_string = response['status_string']
        sys.stdout.write(status_string + '\n')

class InspectPaddrCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_paddr"
    DESCRIPTION = "Inspect the contents of a paddr"

    @staticmethod
    def options(parser):
        parser.add_argument("--pstore-id", type=int, help="Pstore ID",
                required=True)
        parser.add_argument("--addr", type=int, help="Address",
                required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        response = string_response_to_string(inspect.paddr(
            conninfo, credentials, args.pstore_id, args.addr))
        sys.stdout.write(response + '\n')

class InspectBtreeCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_btree"
    DESCRIPTION = "Inspect a btree"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", type=str, help="Btree name",
            required=True)
        parser.add_argument("--all", required=False,
            action="store_true", help="Print all blocks in btree")

    @staticmethod
    def main(conninfo, credentials, args):
        response = string_response_to_string(inspect.btree(
            conninfo, credentials, args.name, args.all))
        sys.stdout.write(response + '\n')

class InspectConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "inspect_config"
    DESCRIPTION = "Inspect the config tree"

    @staticmethod
    def options(parser):
        parser.add_argument("-x", "--hex", dest="use_hex", default=False,
            action="store_true", help="Dump the contents as hex",
            required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        response = inspect.config(conninfo, credentials,
            args.use_hex)

        print string_response_to_string(response)
