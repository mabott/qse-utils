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
import qumulo.rest.task as task

class RunningGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "tasks_running"
    DESCRIPTION = "Get a map of running tasks"

    @staticmethod
    def main(conninfo, credentials, _args):
        print task.running(conninfo, credentials)

class StacksGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "task_stacks"
    DESCRIPTION = "Get stacks of all running tasks"

    @staticmethod
    def main(conninfo, credentials, _args):
        print task.stacks(conninfo, credentials)

class CountersGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "task_counters"
    DESCRIPTION = "Get task debug counters"

    @staticmethod
    def main(conninfo, credentials, _args):
        print task.counters(conninfo, credentials)
