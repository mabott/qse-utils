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
def node_full_quorum(conninfo, credentials):
    method = "GET"
    uri = "/v1/node/quorum/full"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def node_specific_quorum(conninfo, credentials, expected_nodes):
    method = "GET"
    uri = UriBuilder(path="/v1/node/quorum/specific")

    uri.add_query_param('nodes', ','.join(expected_nodes))

    return request.rest_request(conninfo, credentials, method, str(uri))
