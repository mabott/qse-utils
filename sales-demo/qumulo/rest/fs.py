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
def read_fs_stats(conninfo, credentials):
    method = "GET"
    uri = build_fs_uri(None)
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def set_acl(conninfo, credentials, path=None, id_=None, control=None,
            aces=None, if_match=None):
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path).add_query_param("acl")
    if id_ is not None:
        id_ = str(id_)
        uri = build_fs_id_uri(id_).add_query_param("acl")
    if control == None or aces == None:
        raise ValueError("Must specify both control flags and ACEs")

    control = list(control)
    aces = list(aces)
    if_match = if_match if if_match is None else str(if_match)

    config = {'aces': aces, 'control': control}
    method = "PUT"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config, if_match=if_match)

@request.request
def set_attr(conninfo, credentials, mode, owner, group, size,
             modification_time, change_time, path=None, id_=None,
             if_match=None):
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path).add_query_param("attributes")
    if id_ is not None:
        path = str(id_)
        uri = build_fs_id_uri(id_).add_query_param("attributes")
    if if_match:
        if_match = str(if_match)

    method = "PUT"

    config = {
        'mode':
            str(mode),
        'owner':
            str(owner),
        'group':
            str(group),
        'size':
            str(size),
        'modification_time':
            str(modification_time),
        'change_time':
            str(change_time),
    }
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config, if_match=if_match)

@request.request
def get_file_attr(conninfo, credentials, id_):
    method = "GET"
    uri = build_fs_file_uri([id_, "attributes"])
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def set_file_attr(conninfo, credentials, mode, owner, group, size,
                  creation_time, modification_time, change_time, id_,
                  if_match=None):
    uri = build_fs_file_uri([id_, "attributes"])
    if if_match:
        if_match = str(if_match)

    method = "PATCH"

    config = {}
    if mode:
        config['mode'] = str(mode)
    if owner:
        config['owner'] = str(owner)
    if group:
        config['group'] = str(group)
    if size:
        config['size'] = str(size)
    if creation_time:
        config['creation_time'] = str(creation_time)
    if modification_time:
        config['modification_time'] = \
            str(modification_time)
    if change_time:
        config['change_time'] = str(change_time)

    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config, if_match=if_match)

@request.request
def write_file(conninfo, credentials, data_file, path=None, id_=None,
               if_match=None):
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path)
    else:
        id_ = str(id_)
        uri = build_fs_id_uri(id_)

    if_match = if_match if if_match is None else str(if_match)

    method = "PUT"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body_file=data_file, if_match=if_match,
        request_content_type=request.CONTENT_TYPE_BINARY)

@request.request
def get_acl(conninfo, credentials, path=None, id_=None):
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path)
    else:
        id_ = str(id_)
        uri = build_fs_id_uri(id_)

    method = "GET"
    uri.add_query_param("acl")
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def get_attr(conninfo, credentials, path=None, id_=None):
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path)
    else:
        id_ = str(id_)
        uri = build_fs_id_uri(id_)

    method = "GET"
    uri.add_query_param("attributes")
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def get_walk(conninfo, credentials, path):
    assert (path is not None)
    path = str(path)
    uri = build_fs_walk_uri(path)

    method = "GET"
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def read_directory(conninfo, credentials, page_size, path=None, id_=None):
    '''
    @param {int} page_size  How many entries to return
    @param {str} path       Directory to read, by path
    @param {int} id_        Directory to read, by ID
    '''
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        # Ensure there is one trailing slash
        path = path.rstrip("/") + "/"
        uri = build_fs_path_uri(path)
    else:
        id_ = str(id_)
        uri = build_fs_id_uri(id_)

    method = "GET"
    uri.add_query_param("readdir")
    if page_size is not None:
        uri.add_query_param("limit", page_size)
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def read_file(conninfo, credentials, file_, path=None, id_=None):
    assert (path is not None) ^ (id_ is not None)
    if path is not None:
        path = str(path)
        uri = build_fs_path_uri(path)
    else:
        id_ = str(id_)
        uri = build_fs_id_uri(id_)

    method = "GET"
    return request.rest_request(conninfo, credentials, method, str(uri),
        response_content_type=request.CONTENT_TYPE_BINARY, response_file=file_)

@request.request
def create_file(conninfo, credentials, name, dir_path=None, dir_id=None):
    name = str(name)
    if dir_path is not None:
        dir_path = str(dir_path)
        uri = build_fs_path_uri(dir_path)
    else:
        dir_id = str(dir_id)
        uri = build_fs_id_uri(dir_id)

    config = {
        'name': name.rstrip("/"),
        'action': 'CREATE_FILE'
    }

    method = "POST"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def create_directory(conninfo, credentials, name, dir_path=None, dir_id=None):
    name = str(name)
    if dir_path is not None:
        dir_path = str(dir_path)
        uri = build_fs_path_uri(dir_path)
    else:
        dir_id = str(dir_id)
        uri = build_fs_id_uri(dir_id)

    config = {
        'name': name,
        'action': 'CREATE_DIRECTORY'
    }

    method = "POST"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def create_symlink(conninfo, credentials, name, target, dir_path=None,
                   dir_id=None):
    name = str(name)
    target = str(target)
    if dir_path is not None:
        dir_path = str(dir_path)
        uri = build_fs_path_uri(dir_path)
    else:
        dir_id = str(dir_id)
        uri = build_fs_id_uri(dir_id)

    config = {
        'name': name.rstrip("/"),
        'old_path' : target,
        'action': 'CREATE_SYMLINK'
    }

    method = "POST"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def create_link(conninfo, credentials, name, target, dir_path=None,
                dir_id=None):
    name = str(name)
    target = str(target)
    if dir_path is not None:
        dir_path = str(dir_path)
        uri = build_fs_path_uri(dir_path)
    else:
        dir_id = str(dir_id)
        uri = build_fs_id_uri(dir_id)

    config = {
        'name': name.rstrip("/"),
        'old_path' : target,
        'action': 'CREATE_LINK'
    }

    method = "POST"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def rename(conninfo, credentials, name, source, dir_path=None, dir_id=None):
    name = str(name)
    source = str(source)
    if dir_path is not None:
        dir_path = str(dir_path)
        uri = build_fs_path_uri(dir_path)
    else:
        dir_id = str(dir_id)
        uri = build_fs_id_uri(dir_id)

    config = {
        'name': name.rstrip("/"),
        'old_path' : source,
        'action': 'RENAME'
    }

    method = "POST"
    return request.rest_request(conninfo, credentials, method, str(uri),
        body=config)

@request.request
def delete(conninfo, credentials, path):
    path = str(path)

    method = "DELETE"
    uri = build_fs_path_uri(path)
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def read_dir_aggregates(conninfo, credentials, path,
        recursive=False, max_entries=None, max_depth=None, order_by=None):
    method = "GET"
    path = str(path)
    path = path.rstrip("/") + "/"
    uri = build_fs_aggregates_uri(path, recursive)

    method = "GET"
    if max_entries is not None:
        uri.add_query_param('max-entries', max_entries)
    if max_depth is not None:
        uri.add_query_param('max-depth', max_depth)
    if order_by is not None:
        uri.add_query_param('order-by', order_by)
    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def get_file_samples(conninfo, credentials, path, count, by_value):
    method = "GET"

    uri = build_fs_uri(['sample', path])
    uri.add_query_param('by-value', by_value)
    uri.add_query_param('count', count)

    return request.rest_request(conninfo, credentials, method, str(uri))

@request.request
def resolve_paths(conninfo, credentials, ids):
    method = "POST"
    uri = "/v1/fs/resolve"
    return request.rest_request(conninfo, credentials, method, uri, body=ids)

#  _   _      _
# | | | | ___| |_ __   ___ _ __ ___
# | |_| |/ _ \ | '_ \ / _ \ '__/ __|
# |  _  |  __/ | |_) |  __/ |  \__ \
# |_| |_|\___|_| .__/ \___|_|  |___/
#              |_|
#
def build_fs_uri(components):
    uri = UriBuilder(path="/v1/fs")
    if components:
        for component in components:
            uri.add_path_component(component)
    return uri

def build_fs_file_uri(components):
    uri = UriBuilder(path="/v1/fs/file")
    if components:
        for component in components:
            uri.add_path_component(component)
    return uri

def build_fs_path_uri(path):
    if not path.startswith('/'):
        path = '/' + path
    return build_fs_uri(["path", path])

def build_fs_walk_uri(path):
    if not path.startswith('/'):
        path = '/' + path
    return build_fs_uri(["walk", path])

def build_fs_aggregates_uri(path, recursive):
    if not path.startswith('/'):
        path = '/' + path
    if recursive:
        return build_fs_uri(["recursive-aggregates", path])
    else:
        return build_fs_uri(["aggregates", path])

def build_fs_id_uri(id_):
    return build_fs_uri(["id", id_])

# Return an iterator that reads an entire directory.  Each iteration returns a
# page of files, which will be the specified page size or less.
def read_entire_directory(conninfo, credentials, page_size=None, path=None,
                          id_=None):
    # Perform initial read_directory normally.
    result = read_directory(conninfo, credentials, page_size=page_size,
        path=path, id_=id_)
    next_uri = result.data['paging']['next']
    yield result.data

    while next_uri != '':
        # Perform raw read_directory with paging URI.
        result = request.rest_request(conninfo, credentials, "GET", next_uri)
        next_uri = result.data['paging']['next']
        yield result.data

# Return an iterator that walks a file system tree depth-first and pre-order
def tree_walk_preorder(conninfo, credentials, path):
    path = str(path)

    def call_read_dir(conninfo, credentials, path):
        for res in read_entire_directory(conninfo, credentials, path=path):
            if 'files' in res:
                for f in res['files']:
                    yield f
                    if f['type'] == 'FS_FILE_TYPE_DIRECTORY':
                        for ff in call_read_dir(conninfo, credentials,
                                                f['path']):
                            yield ff

    res, _ = get_attr(conninfo, credentials, path)
    yield res
    for f in call_read_dir(conninfo, credentials, path):
        yield f

# Return an iterator that walks a file system tree depth-first and post-order
def tree_walk_postorder(conninfo, credentials, path):
    path = str(path)

    def call_read_dir(conninfo, credentials, path):
        for res in read_entire_directory(conninfo, credentials, path=path):
            if 'files' in res:
                for f in res['files']:
                    if f['type'] == 'FS_FILE_TYPE_DIRECTORY':
                        for ff in call_read_dir(conninfo, credentials,
                                                f['path']):
                            yield ff
                    yield f

    for f in call_read_dir(conninfo, credentials, path):
        yield f
    res, _ = get_attr(conninfo, credentials, path)
    yield res
