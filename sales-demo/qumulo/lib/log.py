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

import sys

DEBUG = False
(LOG_FATAL, LOG_CRITICAL, LOG_INFO, LOG_DEBUG) = (0, 1, 2, 3)
VERBOSITY = LOG_CRITICAL

def is_debug():
    return DEBUG
def set_debug():
    global DEBUG
    global VERBOSITY
    DEBUG = True
    VERBOSITY = LOG_DEBUG

def incr_verbosity():
    global VERBOSITY
    VERBOSITY = max(VERBOSITY + 1, LOG_DEBUG)

def quiet():
    global VERBOSITY
    VERBOSITY = LOG_FATAL

def debug(msg):
    if VERBOSITY >= LOG_DEBUG:
        print msg

def info(msg):
    if VERBOSITY >= LOG_INFO:
        print msg

def critical(msg):
    if VERBOSITY >= LOG_CRITICAL:
        print msg

def fatal(msg):
    if VERBOSITY >= LOG_FATAL:
        print msg
    sys.exit(1)
