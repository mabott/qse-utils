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
def get(conninfo, credentials, key, uid):
    uid = int(uid)

    method = "GET"
    uri = UriBuilder(path="/v1/kv")\
        .add_path_component(uid)\
        .add_path_component(key)
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def put(conninfo, credentials, key, value, uid):
    uid = int(uid)

    method = "PUT"
    uri = UriBuilder(path="/v1/kv").add_path_component(uid)\
          .add_path_component(key)

    config = { 'key' : key, 'value' : value }
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def delete(conninfo, credentials, key, uid):
    uid = int(uid)

    method = "DELETE"
    uri = UriBuilder(path="/v1/kv")\
        .add_path_component(uid)\
        .add_path_component(key)
    return request.rest_request(conninfo, credentials, method, str(uri))
