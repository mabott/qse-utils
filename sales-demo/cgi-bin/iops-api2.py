#!/usr/bin/env python
import sys
import os
import re
import argparse
import json
import math
import random
import re
import datetime
import time
import operator
import cgi
from qumulo.rest_client import RestClient


form = cgi.FieldStorage()

big_tree = {"/":{"name":"/", "children":{}, "total":0}}
keys = {}

# api = {"host":"gravytrain","port":8000,"user":"admin","password":"admin"}
api = json.loads( form.getvalue("api") )
rc = RestClient(api["host"], api["port"])
rc.login(api["user"], api["password"])

heats = ['read', 'write', 'namespace-read', 'namespace-write']
all_heat = {}
for heat in heats:
    big_tree["/"][heat] = 0
    paths = rc.stats.heat(heat)
    for path in paths['entries']:
#        path['path'] = re.sub("/$", "", path['path'])
        if path['path'] not in all_heat:
            all_heat[path['path']] = {'host':api['host'], 'path':path['path'], 'read':0, 'write':0, 'namespace-read':0, 'namespace-write':0, 'total':0}
        all_heat[path['path']]['id'] = path['id']
        all_heat[path['path']][heat] = path['rate']
        all_heat[path['path']]['total'] += path['rate']

def add_to_tree(current_node, parts, dets):
    if len(parts) == 0:
        return
    current_part = parts.pop(0)
    if current_part == "":
        return
    if current_node["name"] == "/":
        current_node["total"] += dets["total"]
        for heat in heats:
            current_node[heat] += dets[heat]

    if current_part not in current_node["children"]:
        current_node["children"][current_part] = {"name":current_part, "children":{}, "total":dets["total"]}
        for heat in heats:
            current_node["children"][current_part][heat] = dets[heat]
    else:
        current_node["children"][current_part]["total"] += dets["total"]
        for heat in heats:
            current_node["children"][current_part][heat] += dets[heat]
    add_to_tree(current_node["children"][current_part], parts, dets)

def walk_and_trim_tree(parent_node, current_node):
    cutem = []
    to_delete = []
    for child in current_node["children"]:
        if grand_total > 0 and current_node["children"][child]["total"]/grand_total <= 0.02:
            to_delete.append(child)
        if current_node["name"] != "/" and current_node["children"][child]["total"] / current_node["total"] > 0.9:
            cutem.append({"from":current_node["name"], "to":child})
        else:
            walk_and_trim_tree(current_node, current_node["children"][child])
    if len(cutem) > 0:
        node_key = cutem[0]["from"] + "/" + cutem[0]["to"]
        parent_node["children"][node_key] = current_node["children"][cutem[0]["to"]]
        parent_node["children"][node_key]["name"] = node_key        
        del parent_node["children"][cutem[0]["from"]]
    for td in to_delete:
        if td in current_node["children"]:
            del current_node["children"][td]

the_ends = []

def walk_and_build_others(parent_node, current_node):
    total_child_iops = {"total":0}
    for heat in heats:
        total_child_iops[heat] = 0
    for child in current_node["children"]:
        walk_and_build_others(current_node, current_node["children"][child])
        total_child_iops["total"] += current_node["children"][child]["total"]
        for heat in heats:
            total_child_iops[heat] += current_node["children"][child][heat]

    if total_child_iops > 0  and  (current_node["total"] - total_child_iops["total"] ) / grand_total >= 0.02:
        current_node["children"]["other"] = {"name":"other", "children":{}, "total":(current_node["total"] - total_child_iops["total"] )}
        for heat in heats:
            current_node["children"]["other"][heat] = current_node[heat] - total_child_iops[heat]
#        print "%s - %s" % (current_node["total"], total_child_iops)

nodes = {}
keyed_nodes = {}
def walk_tree(parent_path, current_node):
    global nodes
    full_path = re.sub("^[/]+", "/", parent_path + "/" + current_node["name"])
    nodes[full_path] = {"id":len(nodes), "name":current_node["name"], "full_path": full_path}
    nodes[full_path]["total"] = current_node["total"]
    for heat in heats:
        nodes[full_path][heat] = current_node[heat]

    for child in current_node["children"]:
        walk_tree(parent_path + "/" + current_node["name"], current_node["children"][child])

links = []
def get_links(parent_path, current_node):
    global nodes
    global links
    current_path = re.sub("^[/]+", "/", parent_path + "/" + current_node["name"])
    for child in current_node["children"]:
        child_path = re.sub("^[/]+", "/", parent_path + "/" + current_node["name"] + "/" + current_node["children"][child]["name"])
        target = nodes[child_path]["id"]
        if re.search("other", child_path):
            ip = random.choice(ips)
            target = nodes[ip]["id"]
            nodes[ip]['total'] += current_node["children"][child]['total']
            for heat in heats:
                nodes[ip][heat] += current_node["children"][child][heat]

        links.append({"source":nodes[current_path]["id"], "target":target, "value":current_node["children"][child]["total"]})
        get_links(parent_path + "/" + current_node["name"], current_node["children"][child])

for path in all_heat:
    parts = path.split("/")
    parts.pop(0)
    if all_heat[path]['total'] >= 1:
        add_to_tree(big_tree["/"], parts, all_heat[path])

grand_total = 0
for i in range(0, 10):
    walk_and_trim_tree({}, big_tree["/"])
    grand_total = big_tree["/"]["total"]

walk_and_build_others({}, big_tree["/"])

walk_tree("/", big_tree["/"])
ips = ["128.61.79.87", "128.61.79.86"]
for ip in ips:
    nodes[ip] = {"id":len(nodes), "name":ip, "full_path": ip, "total": 0, 'namespace-read':0, 'namespace-write':0, 'read':0, 'write':0}
    for heat in heats:
        nodes[ip][heat] = 0

get_links("/", big_tree["/"])
nodes_list = [None] * len(nodes)

for node_id in nodes:
    node = nodes[node_id]
    nodes_list[node["id"]] = node
    keyed_nodes[node["id"]] = {'read':node['read'], 'write':node['write']
                    , 'namespace-read':node['namespace-read'], 'namespace-write':node['namespace-write']
                    , 'total':node['total']}

final_json = json.dumps({"nodes":nodes_list, "links":links, "all":keyed_nodes})
final_str = str(final_json)

print "HTTP/1.1 200 OK"
print "Content-Type: application/json"
print "Content-Length: " + str(len(final_str))
print ""
#print more_str
print final_str
