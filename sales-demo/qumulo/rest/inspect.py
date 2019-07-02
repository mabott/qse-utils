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
from qumulo.lib.uri import UriBuilder

@request.request
def superblock(conninfo, credentials, use_hex=False):
    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/superblock")

    if use_hex:
        uri.add_query_param('hex')

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def metatree(conninfo, credentials, inode_num, begin_off=None,
        end_off=None):
    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/metatree")

    uri.add_path_component(inode_num)

    if begin_off != None:
        uri.add_query_param('begin', str(begin_off))

    if end_off != None:
        uri.add_query_param('end', str(end_off))

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def directory(conninfo, credentials, inode_num):
    method = "GET"
    uri = str(UriBuilder(
              path="/v1/debug/inspect/directory").add_path_component(inode_num))

    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def inode(conninfo, credentials, use_hex=False, verbose=False,
        begin_inode=None, end_inode=None):

    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/inode")

    if use_hex:
        uri.add_query_param('hex')

    if verbose:
        uri.add_query_param('verbose')

    if begin_inode != None:
        uri.add_query_param('begin', str(begin_inode))

    if end_inode != None:
        uri.add_query_param('end', str(end_inode))

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def config(conninfo, credentials, use_hex):
    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/config")

    if use_hex:
        uri.add_query_param('hex')

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def verify(conninfo, credentials):
    method = "POST"
    uri = "/v1/debug/inspect/verify"
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def verify_offline(conninfo, credentials):
    method = "POST"
    uri = "/v1/debug/inspect/verify_offline"
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def verify_status(conninfo, credentials):
    method = "GET"
    uri = "/v1/debug/inspect/verify/status"
    return request.rest_request(conninfo, credentials, method, uri)

@request.request
def paddr(conninfo, credentials, pstore_id, addr):
    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/paddr")

    uri.add_path_component(pstore_id)
    uri.add_path_component(addr)

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def btree(conninfo, credentials, btree_name, verbose):
    method = "GET"
    uri = UriBuilder(path="/v1/debug/inspect/btree")
    uri.add_path_component(btree_name)
    if verbose:
        uri.add_query_param("verbose")

    return request.rest_request(conninfo, credentials, method, str(uri))

