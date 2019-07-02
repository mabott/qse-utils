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
from qumulo.lib.uri import UriBuilder

@request.request
def counters_poll(conninfo, credentials, module, counter):
    method = "GET"
    uri = "/v1/stats/counters/"

    # Expand URI with module and specific counter, if specified
    if module is not None:
        module = str(module)
        uri += module
        if module[-1] != '/':
            uri += '/'
        if counter is not None:
            counter = str(counter)
            uri += counter

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def time_series_get(conninfo, credentials, begin_time=0):
    method = "GET"
    uri = "/v1/stats/time-series/?begin-time={}".format(begin_time)
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def time_series_fill(conninfo, credentials, seconds):
    method = "POST"
    uri = "/v1/debug/time-series/fill"
    body = { "seconds": seconds }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def iops_get(conninfo, credentials, specific_type=None):
    method = "GET"
    uri = UriBuilder(path="/v1/stats/iops")
    if specific_type:
        uri.add_query_param('type', specific_type)

    return request.rest_request(conninfo, credentials, method, str(uri))
