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

@request.request
def dump_memory(conninfo, credentials):
    method = "GET"
    uri = "/v1/debug/memory/dump"
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def leak_pages(conninfo, credentials, num_pages):
    method = "POST"
    uri = "/v1/debug/memory/leak_pages"
    body = { 'num_pages' : int(num_pages) }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def leak_byte(conninfo, credentials):
    method = "POST"
    uri = "/v1/debug/memory/leak_byte"
    return request.rest_request(conninfo, credentials, method, uri)
