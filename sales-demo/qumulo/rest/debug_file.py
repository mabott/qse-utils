# Copyright (c) 2014 Qumulo, Inc.
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

DEFAULT_REPEAT_WRITE_TRANSACTION_SIZE = 128 * 4096

def build_repeat_write_uri(components):
    uri = UriBuilder(path="/v1/debug/file")
    if components:
        for component in components:
            uri.add_path_component(component)
    return uri

@request.request
def repeat_write(conninfo, credentials, path, size, byte,
        transaction_size=None):

    if transaction_size == None:
        transaction_size = DEFAULT_REPEAT_WRITE_TRANSACTION_SIZE

    if not path.startswith('/'):
        path = '/' + path

    method = "PUT"
    uri = build_repeat_write_uri(["repeat_write", path])
    options = {
        'size': str(size),
        'transaction_size': int(transaction_size),
        'byte': int(byte),
    }

    return request.rest_request(conninfo, credentials, method, str(uri),
        body=options)
