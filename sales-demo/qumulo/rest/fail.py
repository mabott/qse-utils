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
import time

@request.request
def point_get(conninfo, credentials, path):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/fail").add_path_component(path))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def point_set(conninfo, credentials, path, program, persist=False):
    if program:
        assert program.endswith(';') or program.endswith('}'), \
            'Non-empty program {} must end with ";" or "}}"'.format(program)
    method = "PUT"
    uri = str(UriBuilder(path="/v1/debug/fail").add_path_component(path))
    config = {'program': program, 'persist': persist}
    return request.rest_request(conninfo, credentials, method, uri, body=config)

@request.request
def point_clear(conninfo, credentials, path):
    method = "DELETE"
    uri = str(UriBuilder(path="/v1/debug/fail").add_path_component(path))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def event_poll(conninfo, credentials, event_id):
    method = "GET"
    uri = str(UriBuilder(path="/v1/debug/fail/event").
        add_path_component(event_id))
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def event_set(conninfo, credentials, event_id):
    method = "PUT"
    uri = str(UriBuilder(path="/v1/debug/fail/event").
        add_path_component(event_id))
    body = {'set': True}
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def event_clear(conninfo, credentials, event_id):
    method = "PUT"
    uri = str(UriBuilder(path="/v1/debug/fail/event").
        add_path_component(event_id))
    body = {'set': False}
    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def event_wait(conninfo, credentials, event_id, poll_interval=0.1):
    while True:
        response = event_poll(conninfo, credentials, event_id)
        data = response[0]
        if 'set' not in data or data['set']:
            break
        time.sleep(poll_interval)
    return response

