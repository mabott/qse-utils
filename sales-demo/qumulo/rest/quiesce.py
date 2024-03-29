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
def deferred(conninfo, credentials):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/quiesce/deferred"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def host_config(conninfo, credentials):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/quiesce/host_config"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def pstore_allocation_cache(conninfo, credentials):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/quiesce/pstore_allocation_cache"))
    return request.rest_request(conninfo, credentials, method, uri)
