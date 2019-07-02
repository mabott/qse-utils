# Copyright (c) 2014 Qumulo, Inc.
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
import qumulo.rest.cpu_profile as cpu_profile

import os
import sys

def options_all_nodes(parser):
    parser.add_argument(
        '--all-nodes', help='Perform this on all nodes.', action='store_true')

class StartPostCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cpu_profile_start'
    DESCRIPTION = 'Start CPU profiling'

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        cpu_profile.start(conninfo, credentials, args.all_nodes)

class StopPostCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cpu_profile_stop'
    DESCRIPTION = 'Stop CPU profiling'

    @staticmethod
    def options(parser):
        options_all_nodes(parser)

    @staticmethod
    def main(conninfo, credentials, args):
        cpu_profile.stop(conninfo, credentials, args.all_nodes)

class DumpGetCommand(qumulo.lib.opts.Subcommand):
    NAME = 'cpu_profile_dump'
    DESCRIPTION = 'Dump raw CPU profile data'

    @staticmethod
    def options(parser):
        parser.add_argument('--file', help='File to receive data', type=str)
        parser.add_argument('--force', help='Overwrite an existing file')

    @staticmethod
    def main(conninfo, credentials, args):
        if args.file:
            if os.path.exists(args.file) and not hasattr(args, 'force'):
                raise ValueError('{} already exists.'.format(args.file))
            with open(args.file, 'w') as f:
                cpu_profile.dump(conninfo, credentials, f)
        else:
            cpu_profile.dump(conninfo, credentials, sys.stdout)
