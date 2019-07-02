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

FIELDS = set((
    'assigned_by',
    'ip_ranges',
    'floating_ip_ranges',
    'netmask',
    'gateway',
    'dns_servers',
    'dns_search_domains'
))

@request.request
def get_cluster_network_config(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/network"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def modify_cluster_network_config(conninfo, credentials, **kwargs):
    method = "PATCH"
    uri = "/v1/conf/network"

    config = { }

    for key, value in kwargs.items():
        assert key in FIELDS
        if value is not None:
            config[key] = value

    # If all the fields are specified, use PUT. PATCH would work, but
    # patch was added in 1.0.18, so this needed for the upgrade
    # test. XXXSU TIMEBOMB.
    if set(kwargs.keys()) == FIELDS:
        method = "PUT"

    return request.rest_request(conninfo, credentials, method, uri, body=config)

@request.request
def list_network_status(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/network/status/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def get_network_status(conninfo, credentials, node):
    method = "GET"
    uri = "/v1/conf/network/status/{}".format(node)

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def get_static_ip_allocation(conninfo, credentials,
        try_ranges=None, try_netmask=None, try_floating_ranges=None):
    method = "GET"
    uri = "/v1/conf/network/static-ip-allocation"

    query_params = []

    if try_ranges:
        query_params.append("try={}".format(try_ranges))
    if try_netmask:
        query_params.append("netmask={}".format(try_netmask))
    if try_floating_ranges:
        query_params.append("floating={}".format(try_floating_ranges))

    if query_params:
        uri = uri + "?" + "&".join(query_params)

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def get_floating_ip_allocation(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/network/floating-ip-allocation"

    return request.rest_request(conninfo, credentials, method, uri)
