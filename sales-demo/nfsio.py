#!/usr/bin/env python

import os
import random
import string
import StringIO

import qnfs
from qumulo.rest_client import RestClient

__author__ = 'mbott'
# API Settings
HOST='192.168.11.147'
PORT='8000'
USER='admin'
PASS='a'
IPADDR = '192.168.11.147'
CONTENTS = StringIO.StringIO()
CONTENTS.write('foo ' * 1000000)
PROCESS_COUNT = 4
NUM_FILES = 4


class Devnull(object):
    def write(self, *_):
        pass


def randomname(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def create_tree(width=5, depth=3, namelength=8, basepath='/', nfs=None):
    if not depth:
        return
    dirnames = [os.path.join(basepath, randomname(namelength)) for i in range(width)]
    for d in dirnames:
        os.mkdir(nfs.get_fullpath(d))
        create_tree(width, depth-1, basepath=os.path.join(basepath, d), nfs=nfs)


if __name__ == '__main__':
    nfsmount = qnfs.NFSMount(IPADDR)
    # This is not really necessary unless we are doing multithreaded calling of the RestClient
    rc = [None] * PROCESS_COUNT
    for i in range(0,PROCESS_COUNT):
        rc[i] = RestClient(HOST, PORT)
        rc[i].login(USER, PASS)

    print "Creating tree"
    nfsmount.create_tree(width=4, depth=2)

    print "Getting a sample of paths"
    fullpaths = []
    for root, dirs, files in os.walk(nfsmount.get_fullpath('/')):
        fullpaths.extend([os.path.join(root,d) for d in dirs])

    # Write 8 files in 20 randomly selected directories
    print "Writing files in randomly selected directories"
    random_dirs = []
    for i in range(20):
        random_dirs.append(random.choice(fullpaths))

    for d in random_dirs:
        for foo in range(NUM_FILES):
            filename = nfsmount.random_name(length=3, words=True) + '.txt'
            nfsmount.write_file(os.path.join(d, filename), CONTENTS)
