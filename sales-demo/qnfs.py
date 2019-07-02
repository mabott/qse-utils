__author__ = 'mbott'

import os
import string
import random
import subprocess

class NFSMount(object):
    def __init__(self, ipaddr=None):
        self.ipaddr = ipaddr
        self.mount_found = False
        self.mount_root = '/Volumes/%s' % self.ipaddr
        self.discover_mount()

    def __nonzero__(self):
        return self.mount_found

    def discover_mount(self):
        """Look in the results of the df command for a mount point that matches our ipaddr"""
        out = subprocess.check_output('df', shell=True)
        if self.ipaddr and self.ipaddr in out:
            self.mount_found = True
        else:
            self.mount_found = False

    def create_mount(self):
        try:
            subprocess.check_output('mkdir /Volumes/%s' % self.ipaddr, shell=True)
        except subprocess.CalledProcessError as e:
            print dir(e)
            if e.returncode == 1:
                pass
            else:
                raise
        subprocess.check_output('mount -t nfs %s:/ /Volumes/%s' % (self.ipaddr, self.ipaddr), shell=True)
        self.discover_mount()

    def unmount(self):
        subprocess.check_output('umount /Volumes/%s' % self.ipaddr, shell=True)
        self.discover_mount()

    def write_file(self, filepath, contents):
        """Write a file at filepath containing contents, a file-like object"""
        with open(filepath, 'w') as f:
            f.write(contents.getvalue())

    def read_file(self, filepath, contents):
        """Fill the contents file-object with the contents of the file at filepath"""
        with open(filepath, 'r') as f:
            contents.write(f.read())

    def get_fullpath(self, filepath):
        return os.path.join(self.mount_root, filepath.lstrip('/'))

    resolve_local_filename = get_fullpath

    def random_name(self, length=8, words=False):
        if not words:
            return ''.join(random.choice(string.lowercase) for i in range(length))
        else:
            return self.random_word(count=length)

    def random_word(self, count=1, delimiter="_"):
        wordlist = []
        for i in range(count):
            wordlist.append(self.get_random_word())
        return delimiter.join(wordlist)

    def get_random_word(self):
        with open('/usr/share/dict/words', 'r') as f:
            line = next(f)
            for num, aline in enumerate(f):
                if random.randrange(num + 2): continue
                line = aline.rstrip()
            return line


    def create_directory(self, dirpath):
        fullpath = self.get_fullpath(dirpath)
        os.mkdir(fullpath)

    def create_tree(self, width=1, depth=1, basepath='/'):
        """
        Make a directory tree width x depth at the root of the mounted fs using random arbitrary names
        Also, ph33r Mike's weak recursion skills
        """
        if not depth:
            return
        for i in range(width):
            dirname = self.random_name(length=2, words=True)
            #print "dirname: %s" % dirname
            target_directory = os.path.join(basepath, dirname)
            #print "target directory: %s" % target_directory
            self.create_directory(target_directory)
            # recurse back into this method, but subtract 1 from depth, and always keep width the same
            self.create_tree(width=width, depth=depth-1, basepath=os.path.join(basepath,dirname))

