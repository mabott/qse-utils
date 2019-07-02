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
import qumulo.rest.trace as trace

import os
import sys

def options_all_nodes(parser):
    parser.add_argument(
        '--all-nodes', help='Perform this on all nodes.', action='store_true')

class SetUpPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "trace_set_up"
    DESCRIPTION = "Set up for tracing"

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        trace.set_up(conninfo, credentials, args.all_nodes)

class TearDownPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "trace_tear_down"
    DESCRIPTION = "Tear down tracing resources"

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        trace.tear_down(conninfo, credentials, args.all_nodes)

class StartPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "trace_start"
    DESCRIPTION = "Start tracing"

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        trace.start(conninfo, credentials, args.all_nodes)

class StopPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "trace_stop"
    DESCRIPTION = "Stop tracing"

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        trace.stop(conninfo, credentials, args.all_nodes)

class DumpGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "trace_dump"
    DESCRIPTION = "Dump the raw json from a trace and reset the trace"

    @staticmethod
    def options(parser):
        parser.add_argument("--file", help="File to receive data", type=str)
        parser.add_argument("--force", help="Overwrite an existing file")

    @staticmethod
    def main(conninfo, credentials, args):
        if args.file:
            if os.path.exists(args.file) and not hasattr(args, "force"):
                raise ValueError("{} already exists.".format(args.file))
            f = open(args.file, "wb")
        else:
            # XXXGW: Should be changed to sys.stdout after request.py is fixed
            f = sys.stdout

        trace.dump(conninfo, credentials, f)
