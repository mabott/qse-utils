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
import qumulo.rest.slots as slots

class FailDiskPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_disk"
    DESCRIPTION = "Force a disk to fail"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Slot ID (N.S)", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        slots.fail_disk(conninfo, credentials, args.slot_id)

class RemoveDiskPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "remove_disk"
    DESCRIPTION = "Force remove a disk by slot ID"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Slot ID (N.S)", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        slots.remove_disk(conninfo, credentials, args.slot_id)

class RemoveDiskTemporaryPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "remove_disk_temporary"
    DESCRIPTION = \
        "Force remove a disk by slot ID temporarily, allow re-insertion later"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Slot ID (N.S)", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        slots.remove_disk_temporary(conninfo, credentials, args.slot_id)

class AddNewDiskPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "add_new_disk"
    DESCRIPTION = \
        "Add a blank, formatted disk by slot ID. Only works on simnodes."

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Slot ID (N.S)", required=True)
        parser.add_argument("--size", help="Size of the disk in blocks",
            required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        slots.add_new_disk(conninfo, credentials, args.slot_id, args.size)

class AddiExistingDiskPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "add_existing_disk"
    DESCRIPTION = \
        "Re-insert existing disk (removed by remove_disk_temporary) by slot ID"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Slot ID (N.S)", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        slots.add_existing_disk(conninfo, credentials, args.slot_id)

class DiskIdsForSlotCommand(qumulo.lib.opts.Subcommand):
    NAME = "disk_ids_for_slot"
    DESCRIPTION = "Returns the virtual disk IDs associated with a device slot"

    @staticmethod
    def options(parser):
        parser.add_argument("--slot-id", help="Device slot ID", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print slots.disk_ids_for_slot(conninfo, credentials, args.slot_id)
