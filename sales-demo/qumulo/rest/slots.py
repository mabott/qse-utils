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
from qumulo.lib.uri import UriBuilder

@request.request
def fail_disk(conninfo, credentials, slot_id):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("fail_disk"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def remove_disk(conninfo, credentials, slot_id):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("remove_disk"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def remove_disk_temporary(conninfo, credentials, slot_id):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("remove_disk_temporary"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def add_new_disk(conninfo, credentials, slot_id, size):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("add_new_disk"))

    # size is a 64 bit integer encoded as a string
    body = { "size": str(size), }
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def add_existing_disk(conninfo, credentials, slot_id):
    method = "POST"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("add_existing_disk"))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def disk_ids_for_slot(conninfo, credentials, slot_id):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/slots")
            .add_path_component(slot_id)
            .add_path_component("disk_ids"))
    return request.rest_request(conninfo, credentials, method, uri)
