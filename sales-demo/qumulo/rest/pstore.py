# Copyright (c) 2012 Qumulo, Inc.
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
def pstore_get(conninfo, credentials, pstore=None):
    method = "GET"
    uri = "/v1/debug/pstore/"
    if pstore:
        uri += pstore

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def pstore_fill_post(conninfo, credentials, pstore,
        unexpired_percentage=100, expired_percentage=0, fast=False):
    body = {
        "fast": fast,
        "unexpired_percentage": unexpired_percentage,
        "expired_percentage": expired_percentage,
    }

    method = "POST"
    uri = "/v1/debug/pstore/{}/fill".format(pstore)

    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def pstore_push_layer_post(conninfo, credentials, pstore):
    method = "POST"
    uri = "/v1/debug/pstore/{}/push-layer".format(pstore)

    return request.rest_request(conninfo, credentials, method, uri)
