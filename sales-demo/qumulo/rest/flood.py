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
def start_rpc_flood(conninfo, credentials, remote, count):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/flood/rpc"))
    body = { 'id' : int(remote),
             'count' : int(count) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def get_flood_status(conninfo, credentials):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/flood/rpc"))
    return request.rest_request(conninfo, credentials, method, uri)
