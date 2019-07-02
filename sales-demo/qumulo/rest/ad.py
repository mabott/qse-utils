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
def list_ad(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/ad-domain"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def poll_ad(conninfo, credentials):
    method = "GET"
    uri = "/v1/conf/ad-domain/monitor"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def join_ad(
        conninfo, credentials, domain, username, password, ou,
        domain_netbios=None):
    method = "POST"
    uri = "/v1/conf/ad-domain/join"

    if domain_netbios is None:
        domain_netbios = ""

    config = {
        "domain":         str(domain),
        "domain_netbios": str(domain_netbios),
        "user":           str(username),
        "password":       str(password),
        "ou":             str(ou)
    }

    return request.rest_request(conninfo, credentials, method, uri, body=config)

@request.request
def leave_ad(conninfo, credentials, domain, username, password):
    method = "POST"
    uri = "/v1/conf/ad-domain/leave"

    # XXXSU: support none for these in the api, also, don't call domain
    # assistant script in that case
    if username is None:
        username = ""
    if password is None:
        password = ""

    config = {
        "domain":   str(domain),
        "user":     str(username),
        "password": str(password)
    }

    return request.rest_request(conninfo, credentials, method, uri, body=config)

@request.request
def cancel_ad(conninfo, credentials):
    method = "POST"
    uri = "/v1/conf/ad-domain/cancel"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def set_ad_machine_account(
    conninfo, credentials, domain, account, password, salt, sid):

    method = "PUT"
    uri = "/v1/conf/ad-settings/machine_account"

    req_body = {
        "domain_name": domain,
        "account_name": account,
        "password": password,
        "salt": salt,
        "sid": sid,
    }

    return request.rest_request(
        conninfo, credentials, method, uri, body=req_body)
