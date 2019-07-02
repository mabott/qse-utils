__author__ = 'mbott'

# stdlib
import os
import unittest
import subprocess
import StringIO

# 3rd party
import qnfs

# IP address of your local NFS mount
MOUNT_ADDRESS = '192.168.11.147'
MOUNT_DIR = '/Volumes/%s' % MOUNT_ADDRESS

"""
Test module for qnfs.py.

TODO:
    Refactor TestQnfs()
    Check for mount presence when writing, bail with a proper error message if it's not there?
"""


def create_local_mount(ipaddr):
    cmd = 'mkdir %s' % MOUNT_DIR
    #print cmd
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            pass
        else:
            raise
    cmd2 = 'mount -t nfs %s:/ %s' % (MOUNT_ADDRESS, MOUNT_DIR)
    #print cmd2
    subprocess.check_call(cmd2 , shell=True)


def local_unmount(ipaddr):
    cmd = 'umount %s' % MOUNT_DIR
    subprocess.check_call(cmd, shell=True)


def cleanup_testfiles(ipaddr):
    cmd = 'rm -rf %s/*' % MOUNT_DIR
    subprocess.check_call(cmd, shell=True)


class TestQnfs(unittest.TestCase):
    def test_instantiate(self):
        nfsmount = qnfs.NFSMount()
        self.assertIsNotNone(nfsmount)

    def test_instantiate_with_target_addr(self):
        targetaddr = '192.168.11.147'
        nfsmount = qnfs.NFSMount(ipaddr=targetaddr)
        self.assertEqual(targetaddr,nfsmount.ipaddr)

    def test_instantiate_and_guess_directory(self):
        targetaddr = '192.168.11.147'
        targetdir = '/Volumes/%s' % targetaddr
        nfsmount = qnfs.NFSMount(ipaddr=targetaddr)
        self.assertEqual(targetdir, nfsmount.mount_root)

    def test_get_fullpath(self):
        filename = 'foo.txt'
        fullpath = os.path.join(MOUNT_DIR, filename)
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        result = nfsmount.get_fullpath(filename)
        self.assertEqual(result, fullpath)

    def test_get_fullpath_leading_slash_on_file(self):
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        filepath = '/foo.txt'
        targetfullpath = '%s/foo.txt' % MOUNT_DIR
        self.assertEqual(targetfullpath, nfsmount.get_fullpath(filepath))

    def test_randomname(self):
        target_length = 8
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        result = nfsmount.random_name(target_length)
        self.assertEqual(target_length, len(result))

    def test_randomname2(self):
        target_length = 16
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        result = nfsmount.random_name(target_length)
        self.assertEqual(target_length, len(result))

    def test_randomname_words(self):
        numwords = 2
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        result = nfsmount.random_name(length=2, words=True)
        wordlist = result.split("_")
        self.assertEqual(numwords, len(wordlist))

    def test_random_word(self):
        dict = open('/usr/share/dict/words', 'r')
        wordlist = [l.rstrip() for l in dict.readlines()]
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        word = nfsmount.random_word()
        print word
        self.assertTrue(word in wordlist)

    def test_multiple_random_words(self):
        dict = open('/usr/share/dict/words', 'r')
        numwords = 2
        wordlist = [l.rstrip() for l in dict.readlines()]
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        word = nfsmount.random_word(count=numwords)
        words = word.split("_")
        self.assertTrue(words[0] in wordlist)
        self.assertEqual(numwords, len(words))


class TestQnfsDiscoverMounts(unittest.TestCase):
    def test_discover_local_mount_fail(self):
        """the object should eval to false until a mount is made/discovered"""
        nfsmount = qnfs.NFSMount()
        self.assertFalse(nfsmount)

    def test_discover_local_mount_success(self):
        """the object should eval to true once a mount is made/discovered"""
        create_local_mount(MOUNT_ADDRESS)
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        self.assertTrue(nfsmount)
        local_unmount(MOUNT_ADDRESS)

    def test_create_local_mount(self):
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        self.assertFalse(nfsmount)
        nfsmount.create_mount()
        self.assertTrue(nfsmount)
        local_unmount(MOUNT_ADDRESS)

    def test_remove_local_mount(self):
        create_local_mount(MOUNT_ADDRESS)
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        self.assertTrue(nfsmount)
        nfsmount.unmount()
        self.assertFalse(nfsmount)


class TestMountedStuff(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        create_local_mount(MOUNT_ADDRESS)

    @classmethod
    def tearDownClass(cls):
        cleanup_testfiles(MOUNT_ADDRESS)
        local_unmount(MOUNT_ADDRESS)

    def test_basic_mount_foo(self):
        self.assertEqual(1, 1)


class TestWriteData(TestMountedStuff):
    def test_write_file(self):
        filename = 'foo.txt'
        filepath = os.path.join(MOUNT_DIR, filename)
        contents = StringIO.StringIO()
        contents.write('foo' * 10)
        #print contents.getvalue()
        nfsmount = qnfs.NFSMount(MOUNT_ADDRESS)
        nfsmount.write_file(filepath, contents)
        with open(filepath, 'r') as f:
            read_contents = f.read()
            f.flush()
            f.close()
        self.assertEqual(read_contents, contents.getvalue())

    def test_read_file(self):
        filename = 'bar.txt'
        filepath = os.path.join(MOUNT_DIR, filename)
        contents = StringIO.StringIO()
        contents.write('bar' * 10)
        nfsmount = qnfs.NFSMount(MOUNT_ADDRESS)
        nfsmount.write_file(filepath, contents)  # we should not be using the object to create this file tbh
        read_contents = StringIO.StringIO()
        #read_contents.write(contents.getvalue())
        nfsmount.read_file(filepath, read_contents)
        #print read_contents.getvalue()
        self.assertEqual(read_contents.getvalue(), contents.getvalue())

    def test_resolve_local_filename(self):
        """Given a path to a file on the fs, return the local filename (including mount path)"""
        qpath = "/foo/bar/baz.txt"
        realpath = "/Volumes/%s/foo/bar/baz.txt" % MOUNT_ADDRESS
        nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)
        self.assertEqual(realpath, nfsmount.resolve_local_filename(qpath))


class TestDirTree(TestMountedStuff):
    def setUp(self):
        self.nfsmount = qnfs.NFSMount(ipaddr=MOUNT_ADDRESS)

    def tearDown(self):
        cleanup_testfiles(MOUNT_ADDRESS)

    def test_create_directory(self):
        dirname = 'baz'
        self.nfsmount.create_directory(dirname)
        # Verify the directory exists
        realpath = self.nfsmount.get_fullpath(dirname)
        self.assertTrue(os.path.isdir(realpath))

    def test_create_tree(self):
        """request creation of a 1 x 1 tree, verify it exists"""
        self.nfsmount.create_tree(width=1, depth=1)
        # Get a directory listing of the root of the file system
        dirlist = os.listdir(self.nfsmount.get_fullpath("/"))
        print dirlist
        self.assertEqual(1, len(dirlist))

    def test_create_tree_wide(self):
        """request creation of a 3 x 1 tree, verify 3 dirs get created"""
        wide = 3
        self.nfsmount.create_tree(width=wide, depth=1)
        dirlist = os.listdir(self.nfsmount.get_fullpath("/"))
        print dirlist
        self.assertEqual(wide, len(dirlist))

    def test_create_tree_deep(self):
        """request creation of a 1 x 3 tree, verify 3 dirs deep get created"""
        deep = 3
        wide = 1
        self.nfsmount.create_tree(width=wide, depth=deep)
        dirlist = os.listdir(self.nfsmount.get_fullpath("/"))
        print dirlist
        self.assertEqual(1, len(dirlist))
        # descend into dirlist[0]
        dirlist2 = os.listdir(self.nfsmount.get_fullpath(dirlist[0]))
        print dirlist2
        self.assertEqual(1, len(dirlist2))
        # descend into dirlist2[0]
        dirlist3 = os.listdir(self.nfsmount.get_fullpath(os.path.join(dirlist[0], dirlist2[0])))
        print dirlist3
        self.assertEqual(1, len(dirlist3))
