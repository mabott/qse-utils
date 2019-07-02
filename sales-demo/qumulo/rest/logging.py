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

import qumulo.lib.request as request

@request.request
def query_logging_config(conninfo, credentials, modulepath):

    "Query logging configuration for specific module"

    method = "GET"
    uri = "/v1/conf/log/module/" + modulepath

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def query_logging_all_config(conninfo, credentials):

    "Query logging configuration for all modules"

    method = "GET"
    uri = "/v1/conf/log/all_modules/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def update_logging_config(conninfo, credentials, modulepath, loglevel):

    "Set/Update logging configuration for a specific module"

    method = "PUT"
    uri = "/v1/conf/log/module/" + modulepath

    if loglevel == 'DEFAULT':
        moduleconfig = {
            'level':  'QM_LOG_INVALID',
            'reset':  True
        }
    else:
        moduleconfig = {
            'level':  str(loglevel),
            'reset':  False
        }

    return request.rest_request(
        conninfo, credentials, method, uri, body=moduleconfig)

@request.request
def list_log_modules(conninfo, credentials):
    "Get a list of modules that offer logging"
    method = "GET"
    uri = "/v1/conf/module/log/"

    return request.rest_request(conninfo, credentials, method, uri)
