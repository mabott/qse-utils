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
import qumulo.rest.fs as fs
import qumulo.lib.request as request

import qumulo.lib.util

import os.path
import sys
import json

AGG_ORDERING_CHOICES = [
    "total_blocks",
    "total_files",
    "total_directories",
    "total_input_ops",
    "moving_blocks",
    "moving_input_ops"]

def all_elements_none(iterable):
    for element in iterable:
        if element is not None:
            return False
    return True

class GetStatsCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_get_stats"
    DESCRIPTION = "Get file system statistics"

    @staticmethod
    def main(conninfo, credentials, _args):
        print fs.read_fs_stats(conninfo, credentials)

class GetAttrCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_get_attr"
    DESCRIPTION = "Get file attributes (deprecated)"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.get_attr(conninfo, credentials, args.path, args.id)

class SetAttrCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_set_attr"
    DESCRIPTION = "Set file attributes (deprecated)"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)
        parser.add_argument("--mode", type=str,
                            help="Posix-style file mode (octal)")
        parser.add_argument("--owner", help="File owner", type=str)
        parser.add_argument("--group", help="File group", type=str)
        parser.add_argument("--size", help="File size", type=str)
        parser.add_argument("--modification-time", type=str,
                            help='File modification time (as RFC 3339 string)')
        parser.add_argument("--change-time", type=str,
                            help='File change time (as RFC 3339 string)')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")
        if all_elements_none([args.mode, args.owner, args.group, args.size,
                              args.modification_time, args.change_time]):
            raise ValueError("Must specify at least one option to change.")

        # Get current attributes
        if args.path:
            attrs, etag = fs.get_attr(conninfo, credentials, args.path)
        elif args.id:
            attrs, etag = fs.get_attr(conninfo, credentials, None,
                                              args.id)

        # Update current attributes based on passed in arguments
        if args.mode is not None:
            attrs['mode'] = args.mode
        if args.owner is not None:
            attrs['owner'] = args.owner
        if args.group is not None:
            attrs['group'] = args.group
        if args.size is not None:
            attrs['size'] = args.size
        if args.modification_time is not None:
            attrs['modification_time'] = args.modification_time
        if args.change_time is not None:
            attrs['change_time'] = args.change_time

        print fs.set_attr(conninfo, credentials,
                attrs['mode'], attrs['owner'], attrs['group'], attrs['size'],
                attrs['modification_time'], attrs['change_time'],
                args.path, args.id, etag)

class GetFileAttrCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_file_get_attr"
    DESCRIPTION = "Get file attributes"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="File id", type=str, required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print fs.get_file_attr(conninfo, credentials, args.id)

class SetFileAttrCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_file_set_attr"
    DESCRIPTION = "Set file attributes"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="File id", type=str, required=True)
        parser.add_argument("--mode", type=str,
                            help="Posix-style file mode (octal)")
        parser.add_argument("--owner", help="File owner", type=str)
        parser.add_argument("--group", help="File group", type=str)
        parser.add_argument("--size", help="File size", type=str)
        parser.add_argument("--creation-time", type=str,
                            help='File creation time (as RFC 3339 string)')
        parser.add_argument("--modification-time", type=str,
                            help='File modification time (as RFC 3339 string)')
        parser.add_argument("--change-time", type=str,
                            help='File change time (as RFC 3339 string)')

    @staticmethod
    def main(conninfo, credentials, args):
        if all_elements_none([args.mode, args.owner, args.group, args.size,
                              args.creation_time, args.modification_time,
                              args.change_time]):
            raise ValueError("Must specify at least one option to change.")

        print fs.set_file_attr(conninfo, credentials,
                args.mode, args.owner, args.group, args.size,
                args.creation_time, args.modification_time, args.change_time,
                args.id)

class GetAclCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_get_acl"
    DESCRIPTION = "Get file ACL"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.get_acl(conninfo, credentials, args.path,
            args.id)

class SetAclCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_set_acl"
    DESCRIPTION = "Set file ACL"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)
        parser.add_argument("--file", help="Local file containing ACL JSON"
                            " containing control flags and ACEs",
                            required=False, type=str)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")
        if not bool(args.file):
            raise ValueError('Must specify --file')

        acl_control = None
        acl_aces = None
        with open(args.file) as f:
            contents = f.read()
            try:
                acl_contents = json.loads(contents)
                acl_control = acl_contents.get("control")
                acl_aces = acl_contents.get("aces")
            except ValueError, e:
                raise ValueError("Error parsing ACL data: %s\n" % str(e))

        etag = None
        print fs.set_acl(conninfo, credentials, path=args.path,
                id_=args.id, control=acl_control, aces=acl_aces,
                if_match=etag)

class CreateFileCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_create_file"
    DESCRIPTION = "Create a new file"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", help="New file name", required=True)
        parser.add_argument("--path", help="Path to parent directory")
        parser.add_argument("--id", help="ID of parent directory")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.create_file(conninfo, credentials, args.name,
            dir_path=args.path, dir_id=args.id)

class CreateDirectoryCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_create_dir"
    DESCRIPTION = "Create a new directory"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", help="New directory name", required=True)
        parser.add_argument("--path", help="Path to parent directory")
        parser.add_argument("--id", help="ID of parent directory")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.create_directory(conninfo, credentials, args.name,
            dir_path=args.path, dir_id=args.id)

class CreateSymlinkCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_create_symlink"
    DESCRIPTION = "Create a new symbolic link"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", help="New symlink name", required=True)
        parser.add_argument("--path", help="Path to parent directory")
        parser.add_argument("--id", help="ID of parent directory")
        parser.add_argument("--target", help="Link target", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.create_symlink(conninfo, credentials, args.name,
            args.target, dir_path=args.path, dir_id=args.id)

class CreateLinkCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_create_link"
    DESCRIPTION = "Create a new link"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", help="New link name", required=True)
        parser.add_argument("--path", help="Path to parent directory")
        parser.add_argument("--id", help="ID of parent directory")
        parser.add_argument("--target", help="Link target", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.create_link(conninfo, credentials, args.name,
            args.target, dir_path=args.path, dir_id=args.id)

class RenameCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_rename"
    DESCRIPTION = "Rename a file system object"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", help="New name", required=True)
        parser.add_argument("--path", help="Path to parent directory")
        parser.add_argument("--id", help="ID of parent directory")
        parser.add_argument("--source", help="Source file path", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        print fs.rename(conninfo, credentials, args.name,
            args.source, dir_path=args.path, dir_id=args.id)

class DeleteCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_delete"
    DESCRIPTION = "Delete a file system object"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        fs.delete(conninfo, credentials, args.path)
        print "File system object was deleted."

class WriteFileCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_write"
    DESCRIPTION = "Write a file"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)
        parser.add_argument("--file", help="File data to send", type=str)
        parser.add_argument("--create", action="store_true",
                            help="Create file before writing (fails if exists)")
        parser.add_argument("--stdin", action="store_true",
                            help="Write file from stdin")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.create:
            raise ValueError("cannot use --create with --id")
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")
        if args.stdin:
            if args.file:
                raise ValueError("--stdin conflicts with --file")
            elif not args.chunked:
                raise ValueError("--stdin must be sent chunked")
        elif args.file:
            if not os.path.isfile(args.file):
                raise ValueError("%s is not a file" % args.file)
        else:
            raise ValueError("Must specify --stdin or --file")

        infile = open(args.file, "rb") if args.file else sys.stdin

        if args.create:
            dirname, basename = qumulo.lib.util.unix_path_split(args.path)
            if not basename:
                raise ValueError("Path has no basename")
            fs.create_file(conninfo, credentials, basename, dirname)

        etag = None
        print fs.write_file(conninfo, credentials, infile,
            args.path, args.id, etag)

class ReadFileCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_read"
    DESCRIPTION = "Read a file"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str)
        parser.add_argument("--id", help="File id", type=str)
        parser.add_argument("--file", help="File to receive data", type=str)
        parser.add_argument("--force", action='store_true',
                            help="Overwrite an existing file")
        parser.add_argument("--stdout", action='store_const', const=True,
                            help="Output data to standard out")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.stdout:
            if args.file:
                raise ValueError("--stdout conflicts with --file")
        elif args.file:
            if os.path.exists(args.file) and not args.force:
                raise ValueError("%s already exists." % args.file)
        else:
            raise ValueError("Must specify --stdout or --file")

        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")

        if args.file is None:
            f = sys.stdout
        else:
            f = open(args.file, "wb")

        fs.read_file(conninfo, credentials, f, path=args.path,
            id_=args.id)
        # Print nothing on success (File may be output into stdout)

class ReadDirectoryCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_read_dir"
    DESCRIPTION = "Read directory"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Directory path", type=str)
        parser.add_argument("--id", help="Directory id", type=str)
        parser.add_argument("--page-size", type=int,
                            help="Max directory entries to return per request")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.id and args.path:
            raise ValueError("--path conflicts with --id")
        elif not args.id and not args.path:
            raise ValueError("Must specify --path or --id")
        elif args.page_size is not None and args.page_size < 1:
            raise ValueError("Page size must be greater than 0")

        page = fs.read_directory(conninfo, credentials, args.page_size,
                                        args.path, args.id)
        print page
        next_uri = json.loads(str(page))["paging"]["next"]
        while next_uri != "":
            page = request.rest_request(conninfo, credentials, "GET", next_uri)
            print page
            next_uri = json.loads(str(page))["paging"]["next"]

class ReadDirectoryCapacityCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_read_dir_aggregates"
    DESCRIPTION = "Read directory aggregation entries"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Directory path", type=str,
            required=True)
        parser.add_argument("--recursive", action="store_true",
            help="Fetch recursive aggregates")
        parser.add_argument("--max-entries",
            help="Maximum number of entries to return", type=int)
        parser.add_argument("--max-depth",
            help="Maximum depth to recurse when --recursive is set", type=int)
        parser.add_argument("--order-by", choices=AGG_ORDERING_CHOICES,
            help="Specify field used for top N selection and sorting")

    @staticmethod
    def main(conninfo, credentials, args):
        print fs.read_dir_aggregates(conninfo, credentials, args.path,
                args.recursive, args.max_entries, args.max_depth, args.order_by)

class TreeWalkCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_walk_tree"
    DESCRIPTION = "Walk file system tree"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to tree root", type=str,
                            required=False, default='/')

    @staticmethod
    def main(conninfo, credentials, args):
        for f in fs.tree_walk_preorder(conninfo, credentials,
                args.path):
            print '%s sz=%s owner=%s group=%s' % (
                f['path'], f['size'], f['owner'], f['group'])

class GetWalkCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_walk"
    DESCRIPTION = "Walk file system path with 1 REST API call"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to file", type=str,
                            required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        if not args.path:
            raise ValueError("Must specify --path")

        print fs.get_walk(conninfo, credentials, args.path)

class TreeDeleteCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_delete_tree"
    DESCRIPTION = "Walk file system tree and delete"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to tree root", type=str,
                            required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        for f in fs.tree_walk_postorder(conninfo, credentials,
                args.path):
            fs.delete(conninfo, credentials, f['path'])
        print "Tree delete was successful."

class GetFileSamplesCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_file_samples"
    DESCRIPTION = "Get a number of sample files from the file system"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", required=True)
        parser.add_argument("--count", type=int, required=True)
        parser.add_argument("--sample-by",
                            choices=['capacity', 'input-ops', 'file'],
                            help="Weight sampling by the given value")

    @staticmethod
    def main(conninfo, credentials, args):
        print fs.get_file_samples(conninfo, credentials, args.path, args.count,
                                  args.sample_by)

class ResolvePathsCommand(qumulo.lib.opts.Subcommand):
    NAME = "fs_resolve_paths"
    DESCRIPTION = "Resolve file IDs to paths"

    @staticmethod
    def options(parser):
        parser.add_argument("--ids", required=True, nargs="*",
            help="File IDs to resolve")

    @staticmethod
    def main(conninfo, credentials, args):
        print fs.resolve_paths(conninfo, credentials, args.ids)
