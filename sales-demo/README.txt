sales-demo - Tools for demonstrating various features of Qumulo QSFS
by Tommy Unger <tommy@qumulo.com>
maintained by Mike Bott <mbott@qumulo.com>


HOWTO:

# Modify the ip address in this file: step1-variables.sh
source step1-variables.sh

# Set up files - will be ready in about 30 seconds, full ready in about 90 seconds
sh step2-setup-create-files.sh

# Heat will start instantly. Afer ~45 seconds you will see a system hog creep into the picture.
sh step3-generate-iops.sh

# launch a local web server
./run-cgi-server
# http://localhost:8000/
# http://localhost:8000/ribbon-graph/


KNOWN ISSUES:

Sometimes, step3-generate-iops.sh can fail because it doesn't receive a file list from the API call. It will fail with a
ValueError because there is nothing in the list to randomly choose from. One can re-run it immediately and it should
work.

Traceback (most recent call last):
  File "demodata.py", line 355, in <module>
    load_it(args.heat, count)
  File "demodata.py", line 207, in load_it
    file_reads = top_files_sorted[random.choice([random.randint(6, 10), 7]) if file_count > 10 else random.randint(0, file_count-1)]
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/random.py", line 241, in randint
    return self.randrange(a, b+1)
  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/random.py", line 217, in randrange
    raise ValueError, "empty range for randrange() (%d,%d, %d)" % (istart, istop, width)
ValueError: empty range for randrange() (0,0, 0)
