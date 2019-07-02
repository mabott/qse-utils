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
def get_config(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/monitoring"

    return request.rest_request(conninfo, credentials, method, uri)

# pylint: disable=unused-argument
@request.request
def set_config(conninfo, credentials, enabled=None, mq_host=None, mq_port=None,
               s3_proxy_host=None, s3_proxy_port=None, period=None,
               vpn_host=None, vpn_enabled=None):
    method = "PATCH"
    uri = "/v1/conf/monitoring"

    config = {}
    for field in ['enabled', 'mq_host', 'mq_port', 's3_proxy_host',
                  's3_proxy_port', 'period', 'vpn_host', 'vpn_enabled']:
        if locals().get(field) is not None:
            config[field] = locals().get(field)

    return request.rest_request(conninfo, credentials, method, uri, body=config)

@request.request
def get_vpn_keys(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/vpn-keys"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def install_vpn_keys(conninfo, credentials, vpn_keys):
    method = "PUT"
    uri = "/v1/conf/vpn-keys"

    return request.rest_request(conninfo, credentials, method, uri,
        body=vpn_keys)
