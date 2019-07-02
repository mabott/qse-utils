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
def list_groups(conninfo, credentials):
    method = "GET"
    uri = "/v1/auth/groups/"

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def add_group(conninfo, credentials, name, gid):
    gid = gid if gid is None else str(gid)

    method = "POST"
    uri = "/v1/auth/groups/"

    group_info = {
        'name': str(name),
        'gid':  gid if gid is not None else '',
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=group_info)

@request.request
def list_group(conninfo, credentials, group_id):
    group_id = int(group_id)

    method = "GET"
    uri = "/v1/auth/groups/%d" % group_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def modify_group(conninfo, credentials, group_id, name, gid, if_match=None):
    group_id = int(group_id)
    name = str(name)
    gid = gid if gid is None else str(gid)
    if_match = if_match if if_match is None else str(if_match)

    method = "PUT"
    uri = "/v1/auth/groups/%d" % group_id

    group_info = {
        'id':   str(group_id),
        'name': name,
        'gid':  gid if gid is not None else '',
    }

    return request.rest_request(conninfo, credentials, method, uri,
        body=group_info, if_match=if_match)

@request.request
def delete_group(conninfo, credentials, group_id):
    group_id = int(group_id)

    method = "DELETE"
    uri = "/v1/auth/groups/%d" % group_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def group_get_members(conninfo, credentials, group_id):
    group_id = int(group_id)

    method = "GET"
    uri = "/v1/auth/groups/%d/members/" % group_id

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def group_add_member(conninfo, credentials, group_id, member_id):
    group_id = int(group_id)
    member_id = member_id if member_id is None else str(member_id)

    method = "POST"
    uri = "/v1/auth/groups/%d/members/" % group_id
    body = { 'member_id' : member_id if member_id is not None else '' }

    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def group_remove_member(conninfo, credentials, group_id, member_id):
    group_id = int(group_id)
    member_id = int(member_id)

    method = "DELETE"
    uri = "/v1/auth/groups/%d/members/%d" % (group_id, member_id)

    return request.rest_request(conninfo, credentials, method, uri)

# TODO This group conversion function should be a REST call, but is not yet.
# Return a group_id from a string that contains either the id or a name
@request.request
def get_id(conninfo, credentials, value):
    # First, try to parse as an integer
    try:
        return request.RestResponse(int(value), 'etag')
    except ValueError:
        pass

    value = str(value)

    # Second, look up the group by name
    data, etag = list_groups(conninfo, credentials)

    for groups in data:
        if groups['name'] == value:
            return request.RestResponse(int(groups['id']), etag)

    raise ValueError('Unable to convert "%s" to a group id' % value)
