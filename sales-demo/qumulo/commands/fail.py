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
import qumulo.rest.fail as fail

class PointGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_point_get"
    DESCRIPTION = "Get a fail point's program"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to fail point", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.point_get(conninfo, credentials, args.path)

class PointSetCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_point_set"
    DESCRIPTION = "Set a fail point's program"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to fail point", required=True)
        parser.add_argument("--program", help="Program", required=True)
        parser.add_argument("--persist", default=False, action="store_true",
            help="Ensure failpoint will persist across reboots")

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.point_set(conninfo, credentials, args.path,
                args.program, args.persist)

class PointClearCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_point_clear"
    DESCRIPTION = "Clear a fail point"

    @staticmethod
    def options(parser):
        parser.add_argument("--path", help="Path to fail point", required=True)

    @staticmethod
    def main(conninfo, credentials, args):
        fail.point_clear(conninfo, credentials, args.path)

class EventPollCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_event_poll"
    DESCRIPTION = "Poll a fail event."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="Event ID", required=True, type=int)

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.event_poll(conninfo, credentials, args.id)

class EventSetCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_event_set"
    DESCRIPTION = "Set a fail event. Any waiters will be woken up."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="Event ID", required=True, type=int)

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.event_set(conninfo, credentials, args.id)

class EventClearCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_event_clear"
    DESCRIPTION = "Unset a fail event."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="Event ID", required=True, type=int)

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.event_clear(conninfo, credentials, args.id)

class EventWaitCommand(qumulo.lib.opts.Subcommand):
    NAME = "fail_event_wait"
    DESCRIPTION = "Wait for the event to be set, then return. " \
        "If the event is set when this is called, it will return immediately."

    @staticmethod
    def options(parser):
        parser.add_argument("--id", help="Event ID", required=True, type=int)

    @staticmethod
    def main(conninfo, credentials, args):
        print fail.event_wait(conninfo, credentials, args.id)
