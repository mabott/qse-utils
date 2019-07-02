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
import qumulo.rest.shutdown as shutdown

def ask(command, target):
    f = raw_input("Are you sure you want to %s the %s (yes/no): " %
                  (command, target))
    if f.lower() == 'no':
        print 'Cancelling the %s request' % command
        return False
    elif f.lower() != 'yes':
        raise ValueError("Please enter 'yes' or 'no'")

    return True

class RestartCommand(qumulo.lib.opts.Subcommand):
    NAME = "restart"
    DESCRIPTION = "Restart the server"

    @staticmethod
    def options(parser):
        parser.add_argument("--force", action='store_true',
                            dest='force', help='Do not prompt')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.force or ask("restart", "server"):
            shutdown.restart(conninfo, credentials)
            print "The server is restarting."

class HaltCommand(qumulo.lib.opts.Subcommand):
    NAME = "halt"
    DESCRIPTION = "Halt the server"

    @staticmethod
    def options(parser):
        parser.add_argument("--force", action='store_true',
                            dest='force', help='Do not prompt')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.force or ask("halt", "server"):
            shutdown.halt(conninfo, credentials)
            print "The server is halting."

class RestartClusterCommand(qumulo.lib.opts.Subcommand):
    NAME = "restart_cluster"
    DESCRIPTION = "Restart the cluster"

    @staticmethod
    def options(parser):
        parser.add_argument("--force", action='store_true',
                            dest='force', help='Do not prompt')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.force or ask("restart", "cluster"):
            shutdown.restart_cluster(conninfo, credentials)
            print "The cluster is restarting."

class HaltClusterCommand(qumulo.lib.opts.Subcommand):
    NAME = "halt_cluster"
    DESCRIPTION = "Halt the cluster"

    @staticmethod
    def options(parser):
        parser.add_argument("--force", action='store_true',
                            dest='force', help='Do not prompt')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.force or ask("halt", "cluster"):
            shutdown.halt_cluster(conninfo, credentials)
            print "The cluster is halting."
