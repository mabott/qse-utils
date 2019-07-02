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

'''
Share commands
'''

import qumulo.lib.opts
import qumulo.lib.util
import qumulo.rest.shares as shares
import qumulo.rest.users as users

def convert_nfs_user_mapping(name):
    convert = {
        'none':         'NFS_MAP_NONE',
        'root':         'NFS_MAP_ROOT',
        'all':          'NFS_MAP_ALL',
        'nfs_map_none': 'NFS_MAP_NONE',
        'nfs_map_root': 'NFS_MAP_ROOT',
        'nfs_map_all':  'NFS_MAP_ALL',
    }

    if name.lower() not in convert:
        raise ValueError('%s is not one of none, root, or all' % (name))
    return convert[name.lower()]

class NFSListSharesCommand(qumulo.lib.opts.Subcommand):
    NAME = "nfs_list_shares"
    DESCRIPTION = "List all NFS shares"

    @staticmethod
    def main(conninfo, credentials, _args):
        print shares.nfs_list_shares(conninfo, credentials)

class SMBListSharesCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_list_shares"
    DESCRIPTION = "List all SMB shares"

    @staticmethod
    def main(conninfo, credentials, _args):
        print shares.smb_list_shares(conninfo, credentials)

class NFSAddShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "nfs_add_share"
    DESCRIPTION = "Add a new NFS share"

    @staticmethod
    def options(parser):
        parser.add_argument("--export-path", type=str, default=None,
            required=True, help="NFS Export path")
        parser.add_argument("--fs-path", type=str, default=None, required=True,
            help="File system path")
        parser.add_argument("--description", type=str, default='',
            help="Description of this export")
        parser.add_argument("--read-only", type=bool, default=False,
            help="Share cannot be used to write to the file system")
        parser.add_argument("--host-restrictions", type=str, default=None,
            help="Restrict allowed hosts.  Comma delimited CIDR or ip range.")
        parser.add_argument("--user-mapping", type=str, default='none',
            help="Map users.  none, root, all.")
        parser.add_argument("--map-to-user-id", type=str, default=0,
            help="User to map to (auth_id or name)")
        parser.add_argument("--create-fs-path", action="store_true",
            help= "Creates the specified file system path if it does not exist")

    @staticmethod
    def main(conninfo, credentials, args):
        user_mapping = convert_nfs_user_mapping(args.user_mapping)

        if user_mapping is not 'NFS_MAP_NONE' and not args.map_to_user_id:
            raise ValueError('--user-mapping requires --map-to-user-id')

        if user_mapping is 'NFS_MAP_NONE' and args.map_to_user_id:
            raise ValueError('--map-to-user-id is only valid when mapping user')

        host_restrictions = [] if args.host_restrictions is None else \
            args.host_restrictions.split(',')

        # Allow either auth_id or user name
        user_id = users.get_id(conninfo, credentials,
            args.map_to_user_id)

        print shares.nfs_add_share(conninfo, credentials,
            args.export_path, args.fs_path, args.description, args.read_only,
            host_restrictions, user_mapping, user_id.data,
            args.create_fs_path)

class SMBAddShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_add_share"
    DESCRIPTION = "Add a new SMB share"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", type=str, default=None, required=True,
            help="Name of share")
        parser.add_argument("--fs-path", type=str, default=None, required=True,
            help="File system path")
        parser.add_argument("--description", type=str, default='',
            help="Description of this share")
        parser.add_argument("--read-only", type=bool, default=False,
            help="Share cannot be used to write to the file system")
        parser.add_argument("--allow-guest-access", type=bool, default=False,
            help="Allow guest access to this share")
        parser.add_argument("--create-fs-path", action="store_true",
            help= "Creates the specified file system path if it does not exist")

    @staticmethod
    def main(conninfo, credentials, args):
        print shares.smb_add_share(conninfo, credentials, args.name,
            args.fs_path, args.description, args.read_only,
            args.allow_guest_access, args.create_fs_path)

class NFSListShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "nfs_list_share"
    DESCRIPTION = "List a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to list")

    @staticmethod
    def main(conninfo, credentials, args):
        print shares.nfs_list_share(conninfo, credentials, args.id)

class SMBListShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_list_share"
    DESCRIPTION = "List a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to list")

    @staticmethod
    def main(conninfo, credentials, args):
        print shares.smb_list_share(conninfo, credentials, args.id)

class NFSModShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "nfs_mod_share"
    DESCRIPTION = "Modify a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to modify")
        parser.add_argument("--export-path", type=str, default=None,
            help="Change NFS export path")
        parser.add_argument("--fs-path", type=str, default=None,
            help="Change file system path")
        parser.add_argument("--description", type=str, default=None,
            help="Description of this export")
        parser.add_argument("--read-only", type=str, default=None,
            help="Change read only")
        parser.add_argument("--host-restrictions", type=str, default=None,
            help="Restrict allowed hosts.  Comma delimited CIDR or ip range.")
        parser.add_argument("--user-mapping", type=str, default=None,
            help="Map users.  none, root, all.")
        parser.add_argument("--map-to-user-id", type=str, default=None,
            help="User to map to (auth_id or name)")
        parser.add_argument("--create-fs-path", action="store_true",
            help= "Creates the specified file system path if it does not exist")

    @staticmethod
    def main(conninfo, credentials, args):
        # Get existing share
        share_info = {}
        share_info, share_info['if_match'] = \
            shares.nfs_list_share(conninfo, credentials, args.id)

        # Modify share
        share_info['id_'] = share_info['id']
        share_info['allow_fs_path_create'] = args.create_fs_path
        del share_info['id']
        if args.export_path is not None:
            share_info['export_path'] = args.export_path
        if args.fs_path is not None:
            share_info['fs_path'] = args.fs_path
        if args.description is not None:
            share_info['description'] = args.description
        if args.read_only is not None:
            share_info['read_only'] = \
                qumulo.lib.util.bool_from_string(args.read_only)
        if args.host_restrictions is not None:
            share_info['host_restrictions'] = args.host_restrictions.split(',')
        if args.user_mapping is not None:
            share_info['user_mapping'] = \
                convert_nfs_user_mapping(args.user_mapping)
        if args.map_to_user_id is not None:
            # Allow either auth_id or user name
            user_id = users.get_id(conninfo, credentials,
                args.map_to_user_id)
            share_info['map_to_user_id'] = str(user_id.data)

        # Ensure mapping arguments are a valid combination
        if share_info['user_mapping'] == 'NFS_MAP_NONE':
            # Mapping = None: ensure ID arg wasn't specified.
            if args.map_to_user_id is not None:
                raise ValueError(
                    '--map-to-user-id is only valid when mapping user')

            # If unspecified, clear it automatically.
            share_info['map_to_user_id'] = '0'
        else:
            # Mapping > None: ensure ID arg isn't 0.
            if share_info['map_to_user_id'] == '0':
                raise ValueError('--user-mapping requires --map-to-user-id')

        print shares.nfs_modify_share(conninfo, credentials,
            **share_info)

class SMBModShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_mod_share"
    DESCRIPTION = "Modify a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to modify")
        parser.add_argument("--name", default=None,
            help="Change SMB share name")
        parser.add_argument("--fs-path", type=str, default=None,
            help="Change file system path")
        parser.add_argument("--description", type=str, default=None,
            help="Change description of this share")
        parser.add_argument("--read-only", type=str, default=None,
            help="Change read only")
        parser.add_argument("--allow-guest-access", type=bool, default=False,
            help="Change guest access to this share")
        parser.add_argument("--create-fs-path", action="store_true",
            help= "Creates the specified file system path if it does not exist")

    @staticmethod
    def main(conninfo, credentials, args):
        share_info = {}
        share_info, share_info['if_match'] = \
            shares.smb_list_share(conninfo, credentials, args.id)

        share_info['id_'] = share_info['id']
        share_info['allow_fs_path_create'] = args.create_fs_path
        del share_info['id']
        if args.name is not None:
            share_info['share_name'] = args.name
        if args.fs_path is not None:
            share_info['fs_path'] = args.fs_path
        if args.description is not None:
            share_info['description'] = args.description
        if args.read_only is not None:
            share_info['read_only'] = \
                qumulo.lib.util.bool_from_string(args.read_only)
        if args.allow_guest_access is not None:
            share_info['allow_guest_access'] = args.allow_guest_access

        print shares.smb_modify_share(conninfo, credentials,
            **share_info)

class NFSDeleteShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "nfs_delete_share"
    DESCRIPTION = "Delete a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to delete")

    @staticmethod
    def main(conninfo, credentials, args):
        shares.nfs_delete_share(conninfo, credentials, args.id)
        print "Share has been deleted."

class SMBDeleteShareCommand(qumulo.lib.opts.Subcommand):
    NAME = "smb_delete_share"
    DESCRIPTION = "Delete a share"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="ID of share to delete")

    @staticmethod
    def main(conninfo, credentials, args):
        shares.smb_delete_share(conninfo, credentials, args.id)
        print "Share has been deleted."
