import argparse
import json
import math
import random
import re
import sys
import time

from multiprocessing import Pool
from qumulo.rest_client import RestClient

existing_dirs = {}
existing_paths = {}


TEST_ACES = [
    {
        "flags": [],
        "rights": [
            "QFS_ACCESS_READ",
            "QFS_ACCESS_READ_EA",
            "QFS_ACCESS_READ_ATTR",
            "QFS_ACCESS_READ_ACL",
            "QFS_ACCESS_WRITE_EA",
            "QFS_ACCESS_WRITE_ATTR",
            "QFS_ACCESS_WRITE_ACL",
            "QFS_ACCESS_WRITE_GROUP",
            "QFS_ACCESS_DELETE",
            "QFS_ACCESS_MODIFY",
            "QFS_ACCESS_EXTEND",
            "QFS_ACCESS_SYNCHRONIZE"
        ],
        "trustee": "999",
        "type": "QFS_ACE_TYPE_ALLOWED"
    },
    {
        "flags": [
            "QFS_ACE_FLAG_OBJECT_INHERIT",
            "QFS_ACE_FLAG_CONTAINER_INHERIT",
            "QFS_ACE_FLAG_NO_PROPAGATE_INHERIT",
            "QFS_ACE_FLAG_INHERIT_ONLY",
            "QFS_ACE_FLAG_INHERITED"
        ],
        "rights": [
            "QFS_ACCESS_READ",
            "QFS_ACCESS_READ_EA",
            "QFS_ACCESS_READ_ATTR",
            "QFS_ACCESS_READ_ACL",
            "QFS_ACCESS_SYNCHRONIZE"
        ],
        "trustee": "998",
        "type": "QFS_ACE_TYPE_ALLOWED"
    },
    {
        "flags": [
            "QFS_ACE_FLAG_OBJECT_INHERIT"
        ],
        "rights": [
            "QFS_ACCESS_READ",
            "QFS_ACCESS_READ_EA",
            "QFS_ACCESS_READ_ATTR",
            "QFS_ACCESS_READ_ACL",
            "QFS_ACCESS_SYNCHRONIZE"
        ],
        "trustee": "100",
        "type": "QFS_ACE_TYPE_ALLOWED"
    }]

TEST_CONTROL = [
    "QFS_ACL_CONTROL_TRUSTED",
    "QFS_ACL_CONTROL_PRESENT",
    ]


def create_dir_api(path):
    global rc
    global existing_dirs
    if path in existing_dirs:
        return
    else:
        parts = path.split("/")
        cur_path = ""
        for cur_dir in parts[1:]:
            if cur_path + "/" + cur_dir not in existing_dirs:
                try:
                    rc[random.randint(0, len(rc)-1)].fs.create_directory(name=cur_dir, dir_path=cur_path)
                    pass
                except:
                    pass
                existing_dirs[cur_path + "/" + cur_dir] = 1
            cur_path = cur_path + "/" + cur_dir

def random_exp(max_digits):
    digits = random.randint(1, max_digits)
    return random.randint(math.pow(10, digits-1), math.pow(10, digits))


def write_to_file(path, the_local_file, byte_count, repeat_write=False):
    global rc
    create_dir_api(path)
    if existing_dirs == {}:
        create_folders("/")
    dir_id = get_id_for_path(path)
    try:
        rc[random.randint(0, len(rc)-1)].fs.create_file(name=the_local_file, dir_id=dir_id)
    except:
        pass
    rc_id = random.randint(0, len(rc)-1)
    if repeat_write:
        rc[rc_id].debug_file.repeat_write(path=path + "/" + the_local_file, size=byte_count, byte=90)
    else:
        file_id = get_id_for_path(path + "/" + the_local_file)
        local_file_name = 'whatevs-w' + str(rc_id) + '.txt'
        with open('/tmp/' + local_file_name, 'w') as f:
            f.write('a' * byte_count)
            f.flush()
        with open('/tmp/' + local_file_name, 'rb') as f:
            rc[rc_id].fs.write_file(f, id_=file_id)

def get_id_for_path(the_local_path):
    global existing_paths
    if the_local_path not in existing_paths:
        attrs = rc[random.randint(0, len(rc)-1)].fs.get_attr(path=the_local_path)
        existing_paths[the_local_path] = int(attrs["id"])
    return existing_paths[the_local_path]


def read_it(id, the_path):
    global rc

    file_id = get_id_for_path(the_path)
    f = open('/tmp/whatevs' + str(id) + '.txt', 'wb')
    rc[id].fs.read_file(f, id_=file_id)


def write_it(id, the_path):
    global rc

    file_names = ['big-movie.mov', 'other-movie.avi', 'old-movie-stuff.mov']
    local_file_name = 'whatevs-w' + str(id) + '.txt'
    with open('/tmp/' + local_file_name, 'w') as f:
        f.write('test ' * random.randint(300000, 600000))
        f.flush()


    new_file_name = the_path.split("/")[-1:][0]
    dest_path = re.sub('/[^/]+$', '', the_path)
    dist_dir_id = get_id_for_path(dest_path)
    dest_file = dest_path + "/" + new_file_name
    dest_file_id = get_id_for_path(dest_file)
    try:
        rc[id].fs.create_file(name=new_file_name, dir_id=dist_dir_id)
    except:
        pass

    with open('/tmp/' + local_file_name, 'rb') as f:
        rc[id].fs.write_file(f, id_=dest_file_id)

    # blank it out
    with open('/tmp/' + local_file_name, 'w') as f:
        f.write('test ' * 10)
        f.flush()

    with open('/tmp/' + local_file_name, 'rb') as f:
        rc[id].fs.write_file(f, id_=dest_file_id)


def ns_read(id, the_path):
    new_path_arr = the_path.split("/")
    new_path = '/'.join(new_path_arr[0:len(new_path_arr)-1])
    dir_id = get_id_for_path(new_path)

    rc[id].fs.read_directory(page_size=1000, id_=dir_id)


def ns_write(id, the_path):
    new_path_arr = the_path.split("/")
    new_file_name = new_path_arr[-1:][0]
    dest_path = '/'.join(new_path_arr[0:len(new_path_arr)-1])
    dist_dir_id = get_id_for_path(dest_path)
    mod_time = '2014-11-19T23:03:57.034033286Z'
    change_time = '2014-11-19T23:03:57.034033286Z'
    rc[id].fs.set_attr(mode=777, owner=1, group=1, size=10000, modification_time=mod_time, change_time=change_time, id_ = dist_dir_id)
    rc[id].fs.set_acl(id_ = dist_dir_id, control=TEST_CONTROL, aces=TEST_ACES)
    rc[id].fs.set_attr(mode=777, owner=2, group=1, size=10000, modification_time=mod_time, change_time=change_time, id_ = dist_dir_id)
    rc[id].fs.set_acl(id_ = dist_dir_id, control=TEST_CONTROL, aces=TEST_ACES)


def load_it(heat, count):
    global process_count

    res = rc[0].fs.get_file_samples('/', 200, 'capacity')  # ['capacity', 'capacity-growth', 'input-ops']
    top_files = {}
    for el in res:
        if not re.search("(Share|NYC)", el['name']):
            top_files[el['name']] = el
    top_files_sorted = sorted(top_files, key=lambda k: int(top_files[k]['capacity_usage']), reverse=True)
    file_count = len(top_files_sorted)
    pool = Pool(processes=process_count)
    delpool = Pool(processes=process_count)
    for i in range(0,count):
        file_reads = top_files_sorted[random.choice([random.randint(6, 14)]) if file_count > 14 else random.randint(0, file_count-1)]
        file_writes = top_files_sorted[random.choice([random.randint(3, 14)]) if file_count > 14 else random.randint(0, file_count-1)]
        ns_reads = top_files_sorted[random.choice([random.randint(2, 14)]) if file_count > 14 else random.randint(0, file_count-1)] 
        ns_writes = top_files_sorted[random.choice([random.randint(4, 24), 8]) if file_count > 14 else random.randint(0, file_count-1)]

        if 'file_read' in heat:
            result = pool.apply_async(read_it, args=(i%process_count, file_reads ))
        if 'file_write' in heat and i % 150 == 0:
            result = pool.apply_async(write_it, args=(i%process_count, file_writes ))
        if 'ns_read' in heat:
            result = pool.apply_async(ns_read, args=(i%process_count, ns_reads ))
        if 'ns_write' in heat:
            result = pool.apply_async(ns_write, args=(i%process_count, ns_writes ))
        if i == int(count * 0.90):
            for i in range(0, 10):
                file_name = "important-file-" + str(i) + "." + random.choice(["mp3", "flac", "txt", "bmp", "jpg", "dat", "log"])
                result = pool.apply_async(write_to_file, args=("/Share/walter/junk", file_name, 7000000))
                resultdel = delpool.apply_async(write_to_file, args=("/Share/walter/junk", file_name, 20000))
    print "Generate IOPS"
    result.get()
    print "Clean up files"
    resultdel.get()
    print "IOPS Complete"

cats = [{"name":"Movies"
            , "assets":[{"name":"Ice Age", "scenes":2, "shots":8, "frames":1, "size":200}
                        , {"name":"Twister", "scenes":4, "shots":10, "frames":13, "size":4}
                        ]
          }
        , {"name":"TV Shows"
                        , "assets":[{"name":"Morning Forecast", "scenes":8, "shots":8, "frames":5, "size":8}
                        ]
          }
        ]
people = ['hazel', 'silas', 'madison', 'walter']
folders = ['/', '/', '/stuff/', '/work/', '/junk/']

def create_folders(path, create=False):
    existing_dirs["/"] = 1
    for cat in cats:
        for asset in cat["assets"]:
            dir_path = path + cat["name"] + "/" + asset["name"]
            if create:
                create_dir_api(dir_path)
            get_id_for_path(dir_path)
            existing_dirs[dir_path] = 1
        existing_dirs[path + cat["name"]] = 1
    for person in people:
        dir_path = path + "Share/" + person
        if create:
            create_dir_api(dir_path)
        get_id_for_path(dir_path)
        existing_dirs[dir_path] = 1
    existing_dirs[path + "Share"] = 1

def create_assets(path, desired_size):
    global process_count

    sizes = 0
    file_count = 0
    pool = Pool(processes=process_count)

    for cat in cats:
        for asset in cat["assets"]:
            for scene in range(0, asset['scenes']):
                for shot in range(0, asset['shots']):
                    for frame in range(0, asset['frames']):
                        file_path = path + cat["name"] + "/" + asset["name"] + "/Scene-" + str(scene).zfill(3) + "/Shot-" + str(shot).zfill(2)
                        the_file = "Frame-" + str(frame).zfill(1) + ".mov"
                        size = int(random_exp(2) * asset["size"] * 3.5 * desired_size)
                        sizes += size
                        file_count += 1
                        result = pool.apply_async(write_to_file, args=(file_path, the_file, size, True))
    print "Files to be created: %s  Total Bytes: %s" % ("{:,}".format(file_count), "{:,}".format(sizes))
    result.get()


def create_files(path, files):
    pool = Pool(processes=process_count)
    for file in files:
        print file["size"]
        result = pool.apply_async(write_to_file, args=(path, file["file"], int(float(file["size"])*1000000 ), True) )
    result.get()


def create_share(path, desired_size):
    global process_count
    pool = Pool(processes=process_count)
    file_names = ['Movie', 'Funny', 'Scary', 'Show', 'Family', 'Video']
    total_size = 0
    file_count = 0
    extensions = ['mp3', 'flac', 'mov']
    biggin1 = False
    biggin2 = False
    for i in range(0,400):
        person = people[random.randint(0, len(people)-1)]
        folder = folders[random.randint(0, len(folders)-1)]
        file_name = file_names[random.randint(0, len(file_names)-1)]
        file_extension = extensions[random.randint(0, len(extensions)-1)]
        the_path = path + "/Share/" + person + folder
        the_file = file_name + "-" + str(i) + "." + file_extension
        file_size = int(random_exp(3) * 0.3 * desired_size)
        if person == 'walter' and folder == '/stuff/' and biggin1 == False:
            file_size = int(62040 * desired_size)
            the_file = the_file.replace(".", "-big.")
            biggin1 = True
        if person == 'walter' and folder == '/junk/' and biggin2 == False:
            file_size = int(12040 * desired_size)
            the_file = the_file.replace(".", "-big.")
            biggin2 = True
        total_size += file_size
        file_count += 1
        result = pool.apply_async(write_to_file, args=(the_path, the_file, file_size, True))
    print "Files to be created: %s  Total Bytes: %s" % ("{:,}".format(file_count), "{:,}".format(total_size))
    result.get()



if __name__ == "__main__":
    process_count = 4
    count = 100

    parser = argparse.ArgumentParser(description='Load and demo data')
    parser.add_argument('--op', required=True)
    parser.add_argument('--api', help='Api params', required=True, type=str)

    parser.add_argument('--heat', help='Heat type (file_read, file_write, ns_read, ns_write)', nargs='+')
    parser.add_argument('--size', help='Size of cluster or files')
    parser.add_argument('--files', help='List of files')
    parser.add_argument('--folder', help='Folder')
    parser.add_argument('--count', help='Number of things or times')
    parser.add_argument('--threads', help='threads')

    args = parser.parse_args()
    api = json.loads(args.api)

    if args.threads is not None:
        process_count = int(args.threads)
    if args.count is not None:
        count = int(args.count)

    rc = [None] * process_count
    for i in range(0,process_count):
        rc[i] = RestClient(api["host"], api["port"])
        rc[i].login(api["user"], api["password"])

    if args.op == 'heat':
        load_it(args.heat, count)

    if args.op == 'create':
        create_assets("/", int(args.size))
        create_share("/", int(args.size)*1.5)

    if args.op == 'files':
        create_dir_api("/" + args.folder)
        pool = Pool(processes=process_count)
        for i in range(0, int(args.count)):
            result = pool.apply_async(write_to_file, args=(args.folder, "important-file-" + str(i) + "." + random.choice(["mp3", "flac", "txt", "bmp", "jpg", "dat", "log"]), args.size))
        result.get()

    if args.op == 'file_list':
        create_files(args.folder, json.loads("[" + args.files + "]"))

