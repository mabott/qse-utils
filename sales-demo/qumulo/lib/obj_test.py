#!/usr/bin/env python
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

import json
import unittest

import qumulo.lib.obj as obj

class ObjectTest(unittest.TestCase):
    def test_empty(self):
        o = obj.Object()
        o.foo = 1
        o.bar = 2

        assert o.foo == 1
        assert o.bar == 2

        # dict access needs to work when json field names are keywords
        assert o['foo'] == 1
        assert o['bar'] == 2

        del o.bar
        assert not hasattr(o, 'bar')

    def test_wrapped_nested(self):
        d = {
            'subobj1': {
                'subobj2': {
                    'val': 3,
                },
                'val': 2,
            },
            'val': 1,
            'stuff': [ 1, 2, 3 ]
        }

        o = obj.Object(d)
        assert d == o.dictionary()

        # test existing stuff
        assert o.val == 1
        assert o.subobj1.val == 2
        assert o.subobj1.subobj2.val == 3
        assert len(o.stuff) == 3
        assert o.stuff[2] == 3

        # change a node
        o.subobj1.subobj2.val = 'three'
        assert o.subobj1.subobj2.val == 'three'
        assert d == o.dictionary()

        # insert level
        o.subobj1.subobj2.subobj3 = {}
        o.subobj1.subobj2.subobj3.val = 4
        assert d == o.dictionary()

        # modify array elem
        o.stuff[2] = 9
        assert o.stuff[2] == 9

        # grow array
        o.stuff.append(22)
        assert len(o.stuff) == 4
        assert o.stuff[-1] == 22

    def test_copy_dictionary(self):
        d = {
            'subobj1': {
                'subobj2': {
                    'val': 3,
                },
                'val': 2,
            },
            'val': 1,
            'stuff': [ 1, 2, 3 ]
        }
        o = obj.dict_to_object(d)
        o.newfield = 22
        assert o != d

    def test_json_to_obj(self):
        str1 = '{ "a": true, "b": [ 9, 1, { "c": "d" } ], "e": 22.5 }'
        o1 = obj.json_to_object(str1)
        str2 = json.dumps(o1.dictionary())
        o2 = obj.json_to_object(str2)
        assert o1 == o2

if __name__ == '__main__':
    import qinternal.check.pycheck as pycheck
    pycheck.main()
