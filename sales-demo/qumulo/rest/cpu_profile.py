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

import qumulo.lib.request as request
from qumulo.lib.uri import UriBuilder

@request.request
def start(conninfo, credentials, all_nodes):
    body = {'all_nodes': all_nodes}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/cpu_profile/start"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def stop(conninfo, credentials, all_nodes):
    body = {'all_nodes': all_nodes}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/cpu_profile/stop"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def dump(conninfo, credentials, file_):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/cpu_profile/dump"))
    return request.rest_request(conninfo, credentials, method, uri,
                                response_file=file_)
