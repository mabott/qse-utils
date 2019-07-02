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

import argparse
import getpass

import os
import importlib
import qumulo.commands

# Make it easy to import all CLI commands
def import_commands():
    cmdlibpath = os.path.dirname(qumulo.commands.__file__)
    for _root, _dirs, files in os.walk(cmdlibpath):
        for filename in files:
            # Exclude files that are not command modules
            if filename in ['test_mixin.py']:
                continue

            # Don't try to load _test.py files since they may depend on the
            # mock module. We don't want users of the CLI to need to have mock
            # installed.
            if (filename.endswith(".py") and not filename.startswith("_")
                and not filename.endswith("_test.py")):
                importlib.import_module("qumulo.commands." + filename[:-3])

# Make it easy to import all REST requests
def import_rest():
    cmdlibpath = os.path.dirname(qumulo.rest.__file__)
    for _root, _dirs, files in os.walk(cmdlibpath):
        for filename in files:

            # Don't try to load _test.py files since they may depend on the
            # mock module. We don't want users of the CLI to need to have mock
            # installed.
            if (filename.endswith(".py") and not filename.startswith("_")
                and not filename.endswith("_test.py")):
                importlib.import_module("qumulo.rest." + filename[:-3])

class Subcommand(object):
    HIDDEN = False

    @staticmethod
    def options(parser):
        pass

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    '''
    Custom subcommand help formatter that suppresses hidden subcommands from
    help.
    '''
    def _format_action(self, action):
        '''
        Override _format_action, which is called during parser.format_help() to
        format a single (sub)command. This implementation simply returns no
        information (empty string) for actions (i.e. (sub)commands) that have
        been suppressed.  The default behavior being overridden simply prints
        "== SUPPRESSED ==" for the action.
        '''
        parts = super(SubcommandHelpFormatter, self)._format_action(action)
        if action.help == argparse.SUPPRESS:
            return ''
        return parts

def parse_options(parser, argv):
    parser.formatter_class = SubcommandHelpFormatter
    subparsers = parser.add_subparsers(
        title="REST API",
        description="Interact with the RESTful API by the command line",
        help="API action", metavar="")

    for cls in sorted(Subcommand.__subclasses__(),
            cmp=lambda cls1, cls2: cmp(cls1.NAME, cls2.NAME)):
        # Add a subparser for each subcommand
        subparser = subparsers.add_parser(cls.NAME, description=cls.DESCRIPTION,
            help=cls.DESCRIPTION if not cls.HIDDEN else argparse.SUPPRESS)

        # Add options particular to the subcommand
        cls.options(subparser)

        # Set the subcommand class
        subparser.set_defaults(request=cls)

    return parser.parse_args(argv)

def add_debug(parser, *args, **kwargs):
    kwargs['help'] = argparse.SUPPRESS
    parser.add_argument(*args, **kwargs)

def read_password(user=None, prompt=None):
    if prompt is not None:
        return getpass.getpass(prompt)
    return getpass.getpass("Enter password for %s: " % user)

# Override argument parser so that we can control the output of argparse. In
# many cases, the default output is not good enough, so we augment that by
# printing out the help.
class ArgumentParserOverride(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        print message
        raise SystemExit(1)
