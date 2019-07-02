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
def set_up(conninfo, credentials, all_nodes, trace_level=0):
    body = {'all_nodes': all_nodes, 'trace_level': trace_level}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/trace/set_up"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def tear_down(conninfo, credentials, all_nodes):
    body = {'all_nodes': all_nodes}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/trace/tear_down"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def start(conninfo, credentials, all_nodes):
    body = {'all_nodes': all_nodes}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/trace/start"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def stop(conninfo, credentials, all_nodes):
    body = {'all_nodes': all_nodes}
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/trace/stop"))
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def dump(conninfo, credentials, file_):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/trace/dump"))
    return request.rest_request(conninfo, credentials, method, uri,
                                response_file=file_)
