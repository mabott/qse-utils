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
def list_users(conninfo, credentials):
    method = "GET"
    uri = "/v1/auth/users/"

    return request.rest_request(conninfo, credentials, method, uri)

# TODO Add user REST call should take a password
@request.request
def add_user(conninfo, credentials, name, primary_group, uid):
    method = "POST"
    uri = "/v1/auth/users/"

    user_info = {
        'name':          str(name),
        'primary_group': str(primary_group),
        'uid':           '' if uid is None else str(uid)
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=user_info)

@request.request
def list_user(conninfo, credentials, user_id):
    user_id = int(user_id)

    method = "GET"
    uri = "/v1/auth/users/%d" % user_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def modify_user(conninfo, credentials, user_id, name, primary_group,
        uid, if_match=None):
    user_id = int(user_id)
    if_match = if_match if if_match is None else str(if_match)

    method = "PUT"
    uri = "/v1/auth/users/%d" % user_id

    user_info = {
        'id':            str(user_id),
        'name':          str(name),
        'primary_group': str(primary_group),
        'uid':           '' if uid is None else str(uid)
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=user_info, if_match=if_match)

@request.request
def delete_user(conninfo, credentials, user_id):
    user_id = int(user_id)

    method = "DELETE"
    uri = "/v1/auth/users/%d" % user_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def list_groups_for_user(conninfo, credentials, user_id):
    user_id = int(user_id)

    method = "GET"
    uri = "/v1/auth/users/%d/groups/" % user_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def set_user_password(conninfo, credentials, user_id, new_password):
    user_id = int(user_id)
    new_password = str(new_password)

    method = "POST"
    uri = "/v1/auth/users/%d/setpassword" % user_id
    body = { 'new_password' : new_password }

    return request.rest_request(conninfo, credentials, method, uri, body=body)

# TODO This user conversion function should be a REST call, but is not yet.
# Return a user_id from a string that contains either the id or a name
@request.request
def get_id(conninfo, credentials, value):
    # First, try to parse as an integer
    try:
        return request.RestResponse(int(value), 'etag')
    except ValueError:
        pass

    value = str(value)

    # Second, look up the user by name
    data, etag = list_users(conninfo, credentials)
    for user in data:
        if user['name'] == value:
            return request.RestResponse(int(user['id']), etag)

    raise ValueError('Unable to convert "%s" to a user id' % value)
