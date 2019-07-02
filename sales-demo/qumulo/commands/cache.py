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
import qumulo.rest.cache as cache

class StartPostCommand(qumulo.lib.opts.Subcommand):
    NAME = "cache_clear"
    DESCRIPTION = "Clear the DLM based caches"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        cache.clear(conninfo, credentials)

class CacheStatsGetCommand(qumulo.lib.opts.Subcommand):
    NAME = "cache_stats_get"
    DESCRIPTION = "Get the page cache stats"

    @staticmethod
    def options(parser):
        pass

    @staticmethod
    def main(conninfo, credentials, _args):
        print cache.get_stats(conninfo, credentials)