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
def get_time(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/time"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def set_time(conninfo, credentials,
                     use_ad_for_primary=None, ntp_servers=None):
    method = "PATCH"
    uri = "/v1/conf/time"

    time_config = {}

    if use_ad_for_primary != None:
        time_config["use_ad_for_primary"] = bool(use_ad_for_primary)

    if ntp_servers != None:
        time_config["ntp_servers"] = list(ntp_servers)

    return request.rest_request(conninfo, credentials, method, uri,
        body=time_config)

@request.request
def get_time_status(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/time/status"

    return request.rest_request(conninfo, credentials, method, uri)
