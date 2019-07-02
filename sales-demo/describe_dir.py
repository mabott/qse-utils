#!/usr/bin/env python
# Copyright (c) 2014 Qumulo, Inc. All rights reserved.
#
# NOTICE: All information and intellectual property contained herein is the
# confidential property of Qumulo, Inc. Reproduction or dissemination of the
# information or intellectual property contained herein is strictly forbidden,
# unless separate prior written permission has been obtained from Qumulo, Inc.

################

'''
This tool will create a description file of a directory tree, or
create a new directory tree given a description file. The description file
contains information about the files in the target directory, such as
filenames, filesizes, permissions, etc.
'''

# Import python libraries
import argparse
import errno
import gzip
import json
import logging
import os
import pipes
import random
import re
import string # pylint: disable=deprecated-module
import subprocess
import sys
import stat
import time

# Constants
DELIM = '\t'
HEADER_START = "%s%s" % ("Filename::", DELIM)
MB = 1024*1024
PLATFORM = False
SYSNAME = os.uname()[0]
if SYSNAME == 'Linux':
    LOCAL_HOST_TYPE = 'workstation'
    PLATFORM = "linux"
elif SYSNAME == 'Darwin':
    LOCAL_HOST_TYPE = 'fusion'
    PLATFORM = "mac"
else:
    raise NotImplementedError("Unknown OS")

PRIVATE_FILENAMES = False
FILES = '__files__'

# Status codes
NOT_IMPLEMENTED = 2
FAIL = 1
SUCCESS = 0

# File types
BLOCK_DEV = 'Block Device'
CHAR_DEV = 'Character Device'
DIR = 'Directory'
FIFO = 'FIFO'
FILE = 'File'
SYMLINK = 'Symbolic Link'
SOCKET = 'Socket'

#### Classes

class FileObj(object):
    '''Create a file object from either os.stat or a line from
    a description file'''

    def __init__(self, fileinfo, fake_parent='', from_desc_file=False):
        self.atime = None
        self.ctime = None
        self.extension = ''
        self.filename_base = None
        self.fsize = None
        self.ftype = 'unknown'
        self.gid = None
        self.inode_num = None
        self.link_target_inode = ''
        self.mode = None
        self.mtime = None
        self.nlink = None
        self.mode_perm = None
        self.path = None
        self.fake_path = None
        self.fake_parent = fake_parent
        self.stat = None
        self.uid = None
        self.valid = False

        # Populate the object from a description line
        if from_desc_file:
            if not self.get_info_from_desc_line(fileinfo):
                self.valid = True

        # Populate the object using os.stat
        else:
            self.path = fileinfo
            if not self.get_inode_info():
                self.valid = True

        logging.debug(self)

    def create(self, target_dir, inodes):
        '''Create a new file object'''
        # Prepend the target_dir (strip any leading /s to make it relative)
        self.path = self.path.strip('/')
        path = os.path.join(target_dir, self.path)

        # Create a regular file
        create_status = NOT_IMPLEMENTED
        if self.ftype == FILE:
            create_status = create_file(path, self.fsize)
            # TBD: hardlinks

        # Create a directory
        elif self.ftype == DIR:
            create_status = create_dir(path)

        # Create a symbolic link
        elif self.ftype == SYMLINK:
            rel_target_file = None
            if inodes.has_key(self.link_target_inode):
                link_target_file = os.path.join(target_dir,
                        inodes[self.link_target_inode])
                rel_target_file = os.path.relpath(link_target_file,
                        os.path.dirname(path))
            create_status = create_symlink(path, rel_target_file)

        # Unimplemented
        elif self.ftype == BLOCK_DEV:
            logging.warn("%s: type %s not yet supported" %
                    (self.path, self.ftype))
        elif self.ftype == CHAR_DEV:
            logging.warn("%s: type %s not yet supported" %
                    (self.path, self.ftype))
        elif self.ftype == FIFO:
            logging.warn("%s: type %s not yet supported" %
                    (self.path, self.ftype))
        elif self.ftype == SOCKET:
            logging.warn("%s: type %s not yet supported" %
                    (self.path, self.ftype))
        else:
            logging.warn("%s: unsupported filetype %s" %
                    (self.path, self.ftype))
        return create_status

    def get_info_from_desc_line(self, line):
        '''Parse a line from a description file'''

        try:
            (self.path,
                    self.extension,
                    self.ftype,
                    self.inode_num,
                    self.nlink,
                    self.link_target_inode,
                    self.fsize,
                    self.mode_perm,
                    self.uid,
                    self.gid,
                    self.atime,
                    self.mtime,
                    self.ctime
                    ) = line.split(DELIM)
            self.fsize = int(self.fsize)
            self.mode_perm = int(self.mode_perm)
            self.uid = int(self.uid)
            self.gid = int(self.gid)
        except ValueError, excpt:
            logging.error("Wonky Line: %s (%s)" % (line, excpt))
            return FAIL
        return SUCCESS

    def get_inode_info(self):
        '''Get inode info for a path'''

        # Get stat info
        try:
            self.stat = os.lstat(self.path)
            self.atime = self.stat.st_atime
            self.ctime = self.stat.st_ctime
            self.fsize = int(self.stat.st_size)
            self.gid = self.stat.st_gid
            self.inode_num = self.stat.st_ino
            self.mode = self.stat.st_mode
            self.mode_perm = oct(self.stat[stat.ST_MODE])
            self.mtime = self.stat.st_mtime
            self.nlink = self.stat.st_nlink
            self.uid = self.stat.st_uid
        except Exception, excpt:
            logging.error("Unable to stat %s (%s)" % (self.path, excpt))
            return FAIL

        # Filename base and extension
        match = re.match(r'(.*)\.(.*)$', os.path.basename(self.path))
        if match:
            self.filename_base = match.group(1)
            self.extension = match.group(2)
        else:
            self.filename_base = os.path.basename(self.path)

        # Private filename
        if PRIVATE_FILENAMES:
            fake_name = ''.join(random.choice(string.ascii_letters)
                    for x in range(len(self.filename_base))) \
                            # pylint: disable=deprecated-module
            dot = '.' if self.extension else ''
            self.fake_path = "%s%s%s" % (os.path.join(self.fake_parent,
                    fake_name), dot, self.extension)
        else:
            self.fake_path = self.path

        # Determine the type of file
        if stat.S_ISDIR(self.mode):
            self.ftype = DIR
        elif stat.S_ISREG(self.mode):
            self.ftype = FILE
        elif stat.S_ISBLK(self.mode):
            self.ftype = BLOCK_DEV
        elif stat.S_ISCHR(self.mode):
            self.ftype = CHAR_DEV
        elif stat.S_ISFIFO(self.mode):
            self.ftype = FIFO
        elif stat.S_ISLNK(self.mode):
            self.ftype = SYMLINK
            # Use the inode number of the target file for security purposes
            try:
                link_target_stat = os.stat(self.path)
                self.link_target_inode = link_target_stat.st_ino
            except OSError, excpt:
                logging.warn("Symlink %s points to file not in the tree"
                        % self.path)
                self.link_target_inode = ''
        elif stat.S_ISSOCK(self.mode):
            self.ftype = SOCKET

        return SUCCESS

    def write_desc_entry(self, desc_fh, header=False):
        '''Write an entry to the description file'''

        if header:
            header_str = HEADER_START
            header_str += "%s%s" % ("File Extension", DELIM)
            header_str += "%s%s" % ("Filetype", DELIM)
            header_str += "%s%s" % ("Inode Number", DELIM)
            header_str += "%s%s" % ("Num Links", DELIM)
            header_str += "%s%s" % ("Link Target", DELIM)
            header_str += "%s%s" % ("Filesize (bytes)", DELIM)
            header_str += "%s%s" % ("Permissions", DELIM)
            header_str += "%s%s" % ("User ID", DELIM)
            header_str += "%s%s" % ("Group ID", DELIM)
            header_str += "%s%s" % ("Access Time", DELIM)
            header_str += "%s%s" % ("Mod Time", DELIM)
            header_str += "%s%s" % ("Change Time", DELIM)
            header_str += "\n"
            desc_fh.write(header_str)

        # Write the file entry
        desc_str = ""
        if PRIVATE_FILENAMES:
            desc_str += "%s%s" % (self.fake_path, DELIM)
        else:
            desc_str += "%s%s" % (self.path, DELIM)
        desc_str += "%s%s" % (self.extension, DELIM)
        desc_str += "%s%s" % (self.ftype, DELIM)
        desc_str += "%s%s" % (self.inode_num, DELIM)
        desc_str += "%s%s" % (self.nlink, DELIM)
        desc_str += "%s%s" % (self.link_target_inode, DELIM)
        desc_str += "%s%s" % (self.fsize, DELIM)
        desc_str += "%s%s" % (self.mode_perm, DELIM)
        desc_str += "%s%s" % (self.uid, DELIM)
        desc_str += "%s%s" % (self.gid, DELIM)
        desc_str += "%s%s" % (self.atime, DELIM)
        desc_str += "%s%s" % (self.mtime, DELIM)
        desc_str += "%s" % (self.ctime)
        desc_str += "\n"
        desc_fh.write(desc_str)

    def __str__(self):
        '''Print the object'''
        desc_str = "\nFile Info:\n"
        desc_str += "%-30s: %s\n" % ("Valid", self.valid)
        desc_str += "%-30s: %s\n" % ("Pathname", self.path)
        desc_str += "%-30s: %s\n" % ("Fake Pathname", self.fake_path)
        desc_str += "%-30s: %s\n" % ("Extension", self.extension)
        desc_str += "%-30s: %s\n" % ("Type", self.ftype)
        desc_str += "%-30s: %s\n" % ("Inode #", self.inode_num)
        desc_str += "%-30s: %s\n" % ("# Links", self.nlink)
        desc_str += "%-30s: %s\n" % ("Link Target", self.link_target_inode)
        desc_str += "%-30s: %s\n" % ("Filesize", self.fsize)
        desc_str += "%-30s: %s\n" % ("Permissions", self.mode_perm)
        desc_str += "%-30s: %s\n" % ("UID", self.uid)
        desc_str += "%-30s: %s\n" % ("GID", self.gid)
        desc_str += "%-30s: %s\n" % ("Atime", self.atime)
        desc_str += "%-30s: %s\n" % ("Mtime", self.mtime)
        desc_str += "%-30s: %s\n" % ("Ctime", self.ctime)
        return desc_str

##### Subroutines

def create_dir(path):
    '''
    Attempt to create the directory path
    '''
    logging.info("Creating dir %s", path)
    try:
        os.makedirs(path)
    except OSError, excpt:
        if excpt.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            logging.error("Error creating directory %s (%s)",
                    path, excpt.strerror)
            sys.exit(1)
    return SUCCESS

def create_symlink(path, target):
    '''Create a symlink path that points to a path that is
    relative to the link'''
    exit_code = SUCCESS
    logging.info("Creating symlink %s -> %s" % (path, target))
    if target:
        os.symlink(target, path)
    else:
        logging.warn("%s points to a file not in the tree" % path)
        exit_code = FAIL
    return exit_code

def create_file(path, size):
    '''
    path    complete path, including filename, of the file to be created
    size    size of the file in bytes
    '''
    exit_code = None
    logging.info("Creating %s (%s)" % (path, sizeof_fmt(size)))

    # Create the parentdir
    parentdir = os.path.dirname(path)
    if not os.path.exists(parentdir):
        create_dir(parentdir)

    # If the file has a zero-length, just open
    if int(size) == 0:
        try:
            open(path, "w")
            exit_code = SUCCESS
        except IOError, excpt:
            exit_code = FAIL
            logging.debug("Failed to create %s (%s)" % (path, excpt))
    else:
        infile = "/dev/urandom"
        if size <= MB:
            bs = size
            count = 1
        else:
            bs = MB
            count = int(size/MB)
        cmd = "dd if=%s of=%s count=%d bs=%s" % (infile,
                pipes.quote(path), count, bs)
        (exit_code, _stdout, stderr) = run_cmd(cmd)
        if exit_code:
            logging.error("Failed to create %s (%s)" % (path, stderr))

    return exit_code

def parse_command_line(argv):
    '''Parse the command line, returning a dictionary of values'''

    desc = 'Save a description of a directory tree, or create a new directory '\
            'tree from a description file.'
    epi = 'Ex: %s -d target_dir -o |-i description_file [options]' % sys.argv[0]
    parser = argparse.ArgumentParser(description=desc, epilog=epi)

    parser.add_argument('--debug', default=False, action='store_true',
            help='Print debug logging.')
    parser.add_argument('--logfile', '-l', default=False,
            help='Log script output to a file.')
    parser.add_argument('--verbose', '-v', default=False, action='store_true',
            help='Run verbosely (default is to run quietly).')

    parser.add_argument('--dir', '-d', metavar='target_dir', dest='target_dir',
            default=None, required=True,
            help='Write/read files to/from target_dir.')
    parser.add_argument('--limit', metavar='N', type=int, default=0,
            dest='limit_entries', help='Write/read only N entries')
    parser.add_argument('--private', action='store_true',
            help='Obfuscate file and directory names.')
    parser.add_argument('--d3', action='store_true', dest='d3_format',
            help='Translate a .tsv file into d3 json format (compact format)')
    parser.add_argument('--pretty', action='store_true', dest='pretty_print',
            help='Pretty print the json output')

    parser.add_argument('--infile', '-i', metavar='input_description_file',
            default=None, dest='input_file',
            help='Create new directory tree from input_description_file')
    parser.add_argument('--outfile', '-o', metavar='description_file',
            default=None, dest='output_file',
            help='Save directory contents to description_file (.tsv format)')

    return parser.parse_args(argv)

def catalog_tree(parent, fake_parent, desc_fh, num_entries, total_bytes,
        limit, num_errors):
    '''
    Recursively walk a directory tree, writing a description of each entry
    to the file
    '''
    if limit and num_entries >= limit:
        return (num_entries, total_bytes, num_errors)

    try:
        for filename in os.listdir(parent):
            path = os.path.join(parent, filename)
            fobj = FileObj(path, fake_parent)
            if fobj.valid:
                fobj.write_desc_entry(desc_fh)
                num_entries = num_entries + 1
                total_bytes = total_bytes + fobj.fsize

                # if we're at the limit, return the passed-in num_errors
                if limit and num_entries >= limit:
                    return (num_entries, total_bytes, num_errors)

                # If it's a directory, recurse into it
                if fobj.ftype == DIR:
                    num_entries, total_bytes, num_errors = \
                        catalog_tree(path, fobj.fake_path, desc_fh, num_entries,
                            total_bytes, limit, num_errors)

                # Progress status
                if not (num_entries % 1000):
                    logging.info("Wrote %d file entries so far (%s)" %
                            (num_entries, sizeof_fmt(total_bytes)))
            else:
                num_errors = num_errors + 1

    except ValueError, excpt:
        logging.error("Error walking directory %s (%s). Skipping."
                % (parent, excpt))

    return (num_entries, total_bytes, num_errors)

def create_tree(input_file, target_dir, limit):
    '''Create a directory tree from a provided description file'''

    # Check for target_dir
    if not target_dir:
        logging.error("Please specify a target directory (--dir)")
        sys.exit(1)

    # Open the input file
    try:
        if re.search(r'\.gz', input_file):
            desc_fh = gzip.open(input_file, 'rb')
        else:
            desc_fh = open(input_file, 'r')
    except IOError, excpt:
        logging.error("Error opening input file %s (%s)", input_file, excpt)
        sys.exit(1)

    # Create an inode/filename table for symlink support
    inodes = {}
    lines = desc_fh.readlines()
    for line in lines:
        # Skip the header line
        if re.match('^Filename::', line):
            continue
        # Skip comments
        if re.match('^#.*$', line):
            continue
        fobj = FileObj(line, from_desc_file=True)
        if fobj.valid:
            inodes[fobj.inode_num] = fobj.path
        logging.debug("Size of {inodes}: %s" % sys.getsizeof(inodes))

    # Process each line of the file
    num_errors = 0
    num_lines_processed = 0
    for line in lines:
        if re.match('^Filename::', line):
            continue
        if re.match('^#.*$', line):
            continue
        fobj = FileObj(line, from_desc_file=True)
        if fobj.valid:
            if fobj.create(target_dir, inodes):
                num_errors = num_errors + 1
        else:
            num_errors = num_errors + 1
        num_lines_processed = num_lines_processed + 1
        if not (num_lines_processed % 100):
            logging.info("Processed %d entries so far...", num_lines_processed)
        if limit and num_lines_processed >= limit:
            break

    # Close the input file
    desc_fh.close()

    logging.debug("lines processed: %s, errors: %s" %
            (num_lines_processed, num_errors))
    return num_errors

def delta_time(start_time):
    '''Given a start time in epoch seconds, determine the elapsed time
    and return it along with a more friendly formatted string'''

    now = time.time()
    delta = float(now - start_time)
    if (delta < 60):
        return(delta, "%.2f seconds" % delta)
    elif (delta < 60 * 60):
        return(delta, "%.2f minutes" % float(delta / 60))
    elif (delta < 60 * 60 * 24):
        return(delta, "%.2f hours" % float(delta / (60 * 60)))
    else:
        return(delta, "%.2f days" % float(delta / (60 * 60 * 24)))

def describe_tree(target_dir, output_file, limit):
    '''Create a description file of the requested directory'''
    num_entries = 0
    total_bytes = 0
    num_errors = 0

    # Open the output file
    # Force a .tsv extension
    if not re.match(r'^.*\.tsv$', output_file):
        output_file = "%s.tsv" % output_file
    try:
        desc_fh = open(output_file, 'w')
    except IOError, excpt:
        logging.error("Error opening output file %s (%s)", output_file, excpt)
        sys.exit(1)

    # Write an entry to the output_file for the parent directory
    try:
        fobj = FileObj(target_dir, '')
        target_dir_fake = fobj.fake_path
        fobj.write_desc_entry(desc_fh, True)
        num_entries = num_entries + 1
        total_bytes = total_bytes + fobj.fsize
    except Exception, excpt:
        logging.error("Failed to stat directory %s (%s)" % (target_dir, excpt))

    # Walk the tree, save info to output_file
    num_catalog_errors = 0
    (num_entries, total_bytes, num_catalog_errors) = catalog_tree(target_dir,
            target_dir_fake, desc_fh, num_entries, total_bytes, limit,
            num_catalog_errors)
    num_errors += num_catalog_errors

    # Close the output file
    logging.info("Saved output file '%s'" % output_file)
    desc_fh.close()

    # gzip the file
    try:
        f_out_name = output_file + '.gz'
        logging.info("Creating gzipped archive '%s'" % f_out_name)
        f_in = open(output_file, 'rb')
        f_out = gzip.open(f_out_name, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
    except Exception, excpt:
        logging.error("Failed to gzip %s (%s)" % (output_file, excpt))
        num_errors += 1

    logging.info("Total entries: %d", num_entries)
    logging.info("Total space used: %s", sizeof_fmt(total_bytes))
    return num_errors

def log_start(logfile, verbose, debug=False):
    '''
    Set up log handling for both a file and the console
    '''

    logger = logging.getLogger()
    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO
    logger.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s (%(levelname)-7s): %(message)s',
            "%Y-%m-%d %H:%M:%S")

    # Set up logging to a file
    if logfile:
        logdir = os.path.dirname(logfile)
        if logdir and not os.path.exists(logdir):
            print "Error: log directory does not exist (%s)" % logdir
            sys.exit(1)

        flhndl = logging.FileHandler(logfile, mode='w')
        flhndl.setLevel(loglevel)
        flhndl.setFormatter(formatter)
        logger.addHandler(flhndl)

    # Set up logging to the console
    cnsl = logging.StreamHandler()
    mode = getattr(logging, "WARNING")
    if verbose:
        mode = getattr(logging, "INFO")
    if debug:
        mode = getattr(logging, "DEBUG")
    cnsl.setLevel(mode)
    cnsl.setFormatter(formatter)
    logger.addHandler(cnsl)

def log_summary(start_time, num_errors, msg=None):
    '''Add a summary to the end of a log file'''

    logging.info("="*30)
    if msg:
        logging.info(msg)
    (_delta, delta_str) = delta_time(start_time)
    logging.info("Elapsed time: %s", delta_str)
    if num_errors:
        if isinstance(num_errors, (int, long)):
            logging.error("Exiting with errors (%d)", num_errors)
        else:
            logging.error("Exiting with errors")

def run_cmd(cmd, responses=None, timeout=None):
    '''Use the subprocess module to run and monitor a command.
    responses is a string or list of strings to send to stdin.
    Return (exit_code, stdout, stderr)'''

    stdout = stderr = ""
    stdin_responses = []
    exit_code = None
    run_time = 0
    p_id = None
    start = time.time()

    # Split out stdin responses into a string
    if responses:
        if isinstance(responses, (list, tuple)):
            stdin_responses = '\n'.join(responses)
        else:
            stdin_responses = responses

    # Run the command
    logging.debug("Running command: '%s'...", cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate(stdin_responses)
    p_id = process.pid
    logging.debug("\tCommand PID: %d" % p_id)
    if timeout:
        time.sleep(timeout)
        if process.poll() is None:
            logging.warn("Cmd %s exceeded the time limit! Killing it." % cmd)
            process.kill()
            exit_code = True
    else:
        exit_code = process.wait()
        stderr = stderr.strip()
        stdout = stdout.strip()

    run_time = (time.time() - start) / 60
    logging.debug("\texit_code: %s, output: (%s), err: (%s), time: %.2f min" %
            (exit_code, stdout, stderr, run_time))
    return (exit_code, stdout, stderr)

def sizeof_fmt(num):
    '''Return the number of bytes in human readable format'''

    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f %s" % (num, 'TB')

def translate_to_d3(input_file, output_file, limit, pretty_print=False):
    '''Turn the contents of the input file into a json file that can
    be read by d3 software. Example format:
    {
     "name": "flare",
     "children": [
      {
       "name": "analytics",
       "children": [
        {
         "name": "cluster",
         "children": [
          {"name": "AgglomerativeCluster", "size": 3938},
          {"name": "CommunityStructure", "size": 3812},
          {"name": "HierarchicalCluster", "size": 6714},
          {"name": "MergeEdge", "size": 743}
         ]
        },
        {
         "name": "graph",
         "children": [
          {"name": "BetweennessCentrality", "size": 3534},
          {"name": "LinkDistance", "size": 5731},
          {"name": "MaxFlowMinCut", "size": 7840},
          {"name": "ShortestPaths", "size": 5914},
          {"name": "SpanningTree", "size": 3416}
         ]
        },
        {
         "name": "optimization",
         "children": [
          {"name": "AspectRatioBanker", "size": 7074}
         ]
        }
       ]
      }, ...
    '''

    # Open the input file
    try:
        desc_fh = open(input_file, 'r')
    except IOError, excpt:
        logging.error("Error opening input file %s (%s)", input_file, excpt)
        sys.exit(1)

    # Create the output file
    if not output_file:
        output_file = input_file.replace('.tsv', '.json')
    try:
        json_fh = open(output_file, 'w')
    except IOError, excpt:
        logging.error("Error opening output file %s (%s)", output_file, excpt)
        sys.exit(1)

    # Read each line of the input file, and add it to the tree structure
    # Note: d3 wants this to be a {} eventually, so we'll transform it later
    tree = []

    # Process each line of the file
    num_errors = 0
    num_lines_processed = 0
    lines = desc_fh.readlines()
    for line in lines:
        # Skip the header and any comment lines
        if re.match('^Filename::', line):
            continue
        if re.match('^#.*$', line):
            continue

        # Create a file object and add the appropriate info to the {tree}
        parent = tree
        fobj = FileObj(line, from_desc_file=True)
        if fobj.valid:
            basename = os.path.basename(fobj.path)
            fobj_dirname = os.path.dirname(fobj.path)
            subdirs = []
            if fobj_dirname:
                subdirs = fobj_dirname.lstrip('/').split('/')

            # Create any subdirs necessary
            for subdir in subdirs:
                child_found = False
                for child in parent:
                    if child['name'] == subdir:
                        parent = child['children']
                        child_found = True
                        break
                if not child_found:
                    parent.append({'name': subdir, 'children': []})
                    parent = parent[len(parent)-1]['children']

            # Add the file or directory
            # replace , in filenames; d3 software may have an issue
            basename = basename.replace(',', '--')
            if fobj.ftype == DIR:
                parent.append({'name': basename, 'children': []})
            elif fobj.ftype == FILE:
                parent.append({
                    'name': basename,
                    'inode_num': fobj.inode_num,
                    'num_links': fobj.nlink,
                    'size': fobj.fsize,
                    'permissions': fobj.mode,
                    'uid': fobj.uid,
                    'gid': fobj.gid,
                    'atime': fobj.atime,
                    'mtime': fobj.mtime,
                    'ctime': fobj.ctime
                    })
        else:
            num_errors = num_errors + 1
        num_lines_processed = num_lines_processed + 1
        if not (num_lines_processed % 10000):
            logging.info("Processed %d lines so far...", num_lines_processed)
        if limit and num_lines_processed >= limit:
            break
    desc_fh.close()

    # Print out the d3 format
    d3_tree = tree[0]
    logging.info("Writing output file...")
    if pretty_print:
        json_fh.write(json.dumps(d3_tree, indent=4))
    else:
        json_fh.write(json.dumps(d3_tree))
    json_fh.close()

    # Summary
    logging.info("%d entries saved to output file %s" %
            (num_lines_processed, output_file))
    return num_errors

### Main subroutine
def main():
    '''
    See module doc for details.
    '''

    # Local variables
    num_errors = 0

    # Set a global start time
    start_time = time.time()

    # Parse the command line
    args = parse_command_line(sys.argv[1:])

    # Set up logging
    log_start(args.logfile, args.verbose, args.debug)

    # Use private filenames?
    global PRIVATE_FILENAMES
    if args.private:
        PRIVATE_FILENAMES = True

    # Create a description file or create a tree
    try:
        if args.input_file:
            if args.d3_format:
                num_errors = translate_to_d3(args.input_file,
                        args.output_file, args.limit_entries, args.pretty_print)
            else:
                num_errors = create_tree(args.input_file,
                        args.target_dir, args.limit_entries)
        elif args.output_file:
            num_errors = describe_tree(args.target_dir,
                    args.output_file, args.limit_entries)
        else:
            logging.warn("Missing either -i or -o")
            sys.exit(1)

    except KeyboardInterrupt:
        logging.warn("Keyboard interrupt caught. Cleaning up.")

    except Exception, excpt:
        logging.error("Something bad happened (%s). Please report this error " \
                "to Qumulo Support." % excpt)

    # Exit with the number of errors found
    log_summary(start_time, num_errors)
    sys.exit(num_errors)

# Main
if __name__ == '__main__':
    main()
