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
import qumulo.lib.util
import qumulo.rest.stats as stats

class GetCountersCommand(qumulo.lib.opts.Subcommand):
    NAME = "counters_poll"
    DESCRIPTION = "Get performance counters. With no parameters, prints " + \
        "all counters."

    @staticmethod
    def options(parser):
        parser.add_argument("-m", "--module",
            help="Module path, e.g. 'rpc'")
        parser.add_argument("-c", "--counter",
            help="Specific counter, e.g. 'requests_errored'")

    @staticmethod
    def main(conninfo, credentials, args):
        if (args.module is None) and (args.counter is not None):
            raise ValueError("Must specify module for a specific counter")

        print stats.counters_poll(conninfo, credentials,
            args.module, args.counter)

class GetTimeSeriesCommand(qumulo.lib.opts.Subcommand):
    NAME = "time_series_get"
    DESCRIPTION = "Get specified time series data."

    @staticmethod
    def options(parser):
        parser.add_argument("-b", "--begin-time", default=0,
            help="Begin time for time series intervals, in epoch seconds")

    @staticmethod
    def main(conninfo, credentials, args):
        print stats.time_series_get(conninfo, credentials, args.begin_time)

class FillTimeSeriesCommand(qumulo.lib.opts.Subcommand):
    NAME = "time_series_fill"
    DESCRIPTION = "Fill time series with generated data."

    @staticmethod
    def options(parser):
        parser.add_argument("-s", "--seconds", type=int, required=True,
            help="Number of seconds of history to fill")

    @staticmethod
    def main(conninfo, credentials, args):
        stats.time_series_fill(conninfo, credentials, args.seconds)

class GetIopsCommand(qumulo.lib.opts.Subcommand):
    NAME = "iops_get"
    DESCRIPTION = "Get the sampled iops from the cluster"

    @staticmethod
    def options(parser):
        parser.add_argument(
            '-t', '--type', type=str, default=None,
            choices=['read', 'write', 'namespace-read', 'namespace-write'],
            help="The specific type of IOPS to get")

    @staticmethod
    def main(conninfo, credentials, args):
        print stats.iops_get(conninfo, credentials, args.type)
