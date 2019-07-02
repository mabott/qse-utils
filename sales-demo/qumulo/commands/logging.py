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
import qumulo.rest.logging as logging

LOG_LEVELS = ('QM_LOG_TRACE', 'QM_LOG_DEBUG', 'QM_LOG_INFO', 'QM_LOG_ERROR',
    'QM_LOG_FATAL', 'default')

def parse_level(arg):
    arg = arg.upper()
    if arg == 'DEFAULT':
        return arg

    if not arg.startswith("QM_LOG_"):
        arg = "QM_LOG_" + arg
    elif not arg.startswith("QM_"):
        arg = "QM_" + arg
    if arg not in LOG_LEVELS:
        raise ValueError("Invalid log level '%s' (valid: %s)" %
                         (arg, ", ".join(LOG_LEVELS)))
    return arg

def fmt_module_log_level(modulepath, config):
    s = "syslog configuration:\n"
    s += "{\n"
    s += "\tmodule : %s\n" % modulepath
    s += "\tlevel  : %s\n" % config['level']
    s += "}\n"
    return s

def fmt_all_module_config(config):
    s = "syslog configuration:\n"
    for module in config[:]:
        s += "{\n"
        s += "\tmodule : %s\n" % module['module_path']
        s += "\tlevel  : %s\n" % module['level']
        s += "}\n"
    return s

def fmt_logger_modules(response):
    s = "Available log modules:\n"
    modules = response[:]
    modules.sort(key=lambda m:
                 [ int(p) if p.isdigit() else p for p in m.split('/') ])
    for module in modules:
        s += "\t" + module + "\n"
    return s

#   ____                                          _
#  / ___|___  _ __ ___  _ __ ___   __ _ _ __   __| |___
# | |   / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` / __|
# | |__| (_) | | | | | | | | | | | (_| | | | | (_| \__ \
#  \____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|___/
#

class QueryLoggingConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "logging_list_config"
    DESCRIPTION = "Return syslog configuration for a specific module"

    @staticmethod
    def options(parser):
        parser.add_argument("-m", "--module", type=str, default="/",
                            required=False, help="Module Path")
        parser.add_argument("-a", "--all", default=False, action="store_true",
                            help="Get configuration for all modules",
                            required=False)

    @staticmethod
    def main(conninfo, credentials, args):
        if args.all:
            config, _ = logging.query_logging_all_config(conninfo,
                credentials)
            print fmt_all_module_config(config)
        else:
            config, _ = logging.query_logging_config(conninfo,
                credentials, args.module)
            print fmt_module_log_level(args.module, config)

class UpdateLoggingConfigCommand(qumulo.lib.opts.Subcommand):
    NAME = "logging_update_config"
    DESCRIPTION = "Set/update syslog configuration for the specified module"

    @staticmethod
    def options(parser):
        parser.add_argument("-m", "--module", type=str, default=None,
                            required=True, help="Module Path")
        parser.add_argument("-l", "--level", type=str, default=None,
                            required=True, help="Log Level")

    @staticmethod
    def main(conninfo, credentials, args):
        logging.update_logging_config(
            conninfo, credentials, args.module, parse_level(args.level))

class ListLoggingModulesCommand(qumulo.lib.opts.Subcommand):
    NAME = "logging_list_modules"
    DESCRIPTION = "Modules that offer logging"

    @staticmethod
    def main(conninfo, credentials, _args):
        modules, _ = logging.list_log_modules(conninfo, credentials)
        print fmt_logger_modules(modules)

