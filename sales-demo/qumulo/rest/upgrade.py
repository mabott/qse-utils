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
def config_get(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/upgrade/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def config_put(conninfo, credentials, install_path, target):
    req = {
        'install_path': str(install_path),
        'target': str(target),
    }

    method = "PUT"
    uri = "/v1/conf/upgrade/"

    return request.rest_request(conninfo, credentials, method, uri, body=req)

@request.request
def status_get(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/upgrade/status/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def scanner_status_get(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/upgrade/scanner/status"

    return request.rest_request(conninfo, credentials, method, uri)
