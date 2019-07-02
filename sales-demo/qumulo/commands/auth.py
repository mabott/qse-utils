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
import qumulo.rest.auth as auth
import qumulo.rest.users as users
import qumulo.rest.groups as groups

def list_user(conninfo, credentials, user_id):
    user = users.list_user(conninfo, credentials, user_id)
    user_groups = users.list_groups_for_user(conninfo, credentials,
        user_id)

    # Print out results only on success of both rest calls
    print '%s\nUser %d is a member of following groups: %s' % (
        user, int(user_id), user_groups)

def list_group(conninfo, credentials, group_id):
    group = groups.list_group(conninfo, credentials, group_id)
    members = groups.group_get_members(conninfo, credentials, group_id)

    print '%s\nGroup %d has the following members: %s' % (
        group, int(group_id), members)

#  _   _                  ____                                          _
# | | | |___  ___ _ __   / ___|___  _ __ ___  _ __ ___   __ _ _ __   __| |___
# | | | / __|/ _ \ '__| | |   / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
# | |_| \__ \  __/ |    | |__| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  \___/|___/\___|_|     \____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
#

class ChangePasswordCommand(qumulo.lib.opts.Subcommand):
    NAME = "change_password"
    DESCRIPTION = "Change your password"

    @staticmethod
    def options(parser):
        parser.add_argument(
            "-o", "--old-password", type=str, default=None,
            help="Your old password (insecure, visible via ps)")
        parser.add_argument(
            "-p", "--new-password", type=str, default=None,
            help="Your new password (insecure, visible via ps)")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.old_password is not None:
            old_password = args.old_password
        else:
            old_password = \
                qumulo.lib.opts.read_password(prompt="Old password: ")
        if args.new_password is not None:
            new_password = args.new_password
        else:
            new_password = \
                qumulo.lib.opts.read_password(prompt="New password: ")

        auth.change_password(
            conninfo, credentials, old_password, new_password)
        print "Your password has been changed."

class SetUserPasswordCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_set_password"
    DESCRIPTION = "Set a user's password"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of user to modify")
        parser.add_argument("-p", "--password", type=str, default=None,
            help="The user's new password (insecure, visible via ps)")

    @staticmethod
    def main(conninfo, credentials, args):
        user_id = users.get_id(conninfo, credentials, args.id)

        if args.password is not None:
            password = args.password
        else:
            password = \
                qumulo.lib.opts.read_password("New password for %s: " % args.id)

        users.set_user_password(conninfo, credentials, user_id.data,
            password)
        print "Changed password for %s" % args.id

class ListUsersCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_list_users"
    DESCRIPTION = "List all users"

    @staticmethod
    def main(conninfo, credentials, _args):
        print users.list_users(conninfo, credentials)

class AddUserCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_add_user"
    DESCRIPTION = "Add a new user"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", type=str, default=None,
            help="New user's name (windows style)", required=True)
        parser.add_argument("--primary-group", type=str, default=0,
            help="name or id of primary group (default is Users)")
        parser.add_argument("--uid", type=int, default=None,
            help="optional NFS uid")
        parser.add_argument("-p", "--password", type=str, nargs='?',
            const=True, default=None,
            help="Set user password; reads password from terminal if omitted")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.password is True:
            password = qumulo.lib.opts.read_password(args.name)
        elif args.password is not None:
            password = args.password

        group_id = groups.get_id(conninfo, credentials, args.primary_group)

        res = users.add_user(conninfo, credentials, args.name,
            group_id.data, args.uid)
        print res

        # Set new user's password, ignoring output.
        if args.password is not None:
            user_id = int(res.lookup('id'))
            users.set_user_password(conninfo, credentials, user_id,
                password)

class ListUserCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_list_user"
    DESCRIPTION = "List a user"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of user to modify")

    @staticmethod
    def main(conninfo, credentials, args):
        user_id = users.get_id(conninfo, credentials, args.id)
        list_user(conninfo, credentials, user_id.data)

class ModUserCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_mod_user"
    DESCRIPTION = "Modify a user"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of user to modify")
        parser.add_argument("--name", default=None, help="Change user's name")
        parser.add_argument("--primary-group", type=str, default=None,
            help="Change the user's primary group")
        parser.add_argument("--uid", type=str, default=None,
            help="Change the user's NFS uid (or specify \"none\" to remove)")
        parser.add_argument("--add-group", type=str, default=None,
            help="Add this user to a group")
        parser.add_argument("--remove-group", type=str, default=None,
            help="Remove this user from a group")

    @staticmethod
    def main(conninfo, credentials, args):
        # Get the user object
        user_id = users.get_id(conninfo, credentials, args.id)
        user_info, etag = users.list_user(conninfo, credentials,
            user_id.data)

        # Modify the user object according to specified arguments
        name = user_info['name']
        if args.name is not None:
            name = args.name

        primary_group = user_info['primary_group']
        if args.primary_group is not None:
            primary_group = str(groups.get_id(
                conninfo, credentials, args.primary_group).data)

        uid = user_info['uid']
        if args.uid is not None:
            uid = args.uid.strip()
            if uid.lower() == 'none':
                uid = ''

        # Set the user object, ignore output
        users.modify_user(conninfo, credentials, user_id.data, name,
            primary_group, uid, etag)

        # Add specified groups, ignore output
        if args.add_group:
            group_id = groups.get_id(conninfo, credentials,
                args.add_group)
            groups.group_add_member(conninfo, credentials,
                group_id.data, user_id.data)

        # Remove specified groups, ignore output
        if args.remove_group:
            group_id = groups.get_id(conninfo, credentials,
                args.remove_group)
            groups.group_remove_member(conninfo, credentials,
                group_id.data, user_id.data)

        # Print out the new user object
        list_user(conninfo, credentials, user_id.data)

class DeleteUserCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_delete_user"
    DESCRIPTION = "Delete a user"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of user to delete")

    @staticmethod
    def main(conninfo, credentials, args):
        user_id = users.get_id(conninfo, credentials, args.id)
        users.delete_user(conninfo, credentials, user_id.data)
        print "User was deleted."

#   ____
#  / ___|_ __ ___  _   _ _ __
# | |  _| '__/ _ \| | | | '_ \
# | |_| | | | (_) | |_| | |_) |
#  \____|_|  \___/ \__,_| .__/
#                       |_|
#   ____                                          _
#  / ___|___  _ __ ___  _ __ ___   __ _ _ __   __| |___
# | |   / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
# | |__| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  \____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
#

class ListGroupsCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_list_groups"
    DESCRIPTION = "List all groups"

    @staticmethod
    def main(conninfo, credentials, _args):
        print groups.list_groups(conninfo, credentials)

class AddGroupCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_add_group"
    DESCRIPTION = "Add a new group"

    @staticmethod
    def options(parser):
        parser.add_argument("--name", type=str, default=None,
            help="New group's name (windows style)")
        parser.add_argument("--gid", type=int, default=None,
            help="Optional NFS gid")

    @staticmethod
    def main(conninfo, credentials, args):
        print groups.add_group(conninfo, credentials, args.name,
            args.gid)

class ListGroupCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_list_group"
    DESCRIPTION = "List a group"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of group to list")

    @staticmethod
    def main(conninfo, credentials, args):
        group_id = groups.get_id(conninfo, credentials, args.id)
        list_group(conninfo, credentials, group_id.data)

class ModGroupCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_mod_group"
    DESCRIPTION = "Modify a group"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of group to modify")
        parser.add_argument("--name", default=None, help="Change group's name")
        parser.add_argument("--gid", type=str, default=None,
            help="Change the user's NFS gid (or specify \"none\" to remove)")

    @staticmethod
    def main(conninfo, credentials, args):
        # Get the group object
        group_id = groups.get_id(conninfo, credentials, args.id)
        group_info, etag = groups.list_group(conninfo, credentials,
            group_id.data)

        # Modify the group object according to specified arguments
        name = group_info['name']
        if args.name is not None:
            name = args.name

        gid = group_info['gid']
        if args.gid is not None:
            gid = args.gid.strip()
            if gid.lower() == 'none':
                gid = ''

        # Set the group object, ignore output
        groups.modify_group(conninfo, credentials, group_id.data,
            name, gid, etag)

        # Print out the new group object
        list_group(conninfo, credentials, group_id.data)

class DeleteGroupCommand(qumulo.lib.opts.Subcommand):
    NAME = "auth_delete_group"
    DESCRIPTION = "Delete a group"

    @staticmethod
    def options(parser):
        parser.add_argument("--id", type=str, default=None, required=True,
            help="Name or ID of group to delete")

    @staticmethod
    def main(conninfo, credentials, args):
        group_id = groups.get_id(conninfo, credentials, args.id)
        groups.delete_group(conninfo, credentials, group_id.data)
        print "Group was deleted."
