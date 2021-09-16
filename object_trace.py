import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')
#./bin/radosgw-admin bucket list --bucket test-bucket
object_list = subprocess.run(["./bin/radosgw-admin", "bucket", "list", "--bucket", "test-bucket"], stdout=subprocess.PIPE, text=True)
objects = json.loads(object_list.stdout)
rows = []
headers = ["Name", "Size", "AccountedSize", "Diff", "ObjSize", "ManifestSize", "ManifestHeadSize", "ManifestHeadMax", "BeginStripeSize", "BeginCurStripe", "EndStripeSize", "EndCurStripe"]
for object in objects:
    name = object['name']
    size_actual =  object['meta']['size']
    size_accounted =  object['meta']['accounted_size']
    size_diff = size_accounted - size_actual
    object_stat = subprocess.run(["./bin/radosgw-admin", "object", "stat", "--bucket", "test-bucket", "--object", name], stdout=subprocess.PIPE, text=True)
    stats = json.loads(object_stat.stdout)
    size_obj = stats['size']
    size_man = stats['manifest']['obj_size']
    size_head_man = stats['manifest']['head_size']
    size_head_man_max = stats['manifest']['max_head_size']
    begin_stripe_size = stats['manifest']['begin_iter']['stripe_size']
    begin_cur_stripe = stats['manifest']['begin_iter']['cur_stripe']
    end_stripe_size = stats['manifest']['end_iter']['stripe_size']
    end_cur_stripe = stats['manifest']['end_iter']['cur_stripe']
    rows.append([name, size_actual, size_accounted, size_diff, size_obj, size_man, size_head_man, size_head_man_max, begin_stripe_size, begin_cur_stripe, end_stripe_size, end_cur_stripe])
    #print(name, size_actual, size_accounted, size_diff, size_obj, size_man, size_head_man, size_head_man_max, begin_stripe_size, begin_cur_stripe, end_stripe_size, end_cur_stripe)
    #print("Name: {}, Size: {}, AccountedSize: {}, Diff: {}, ObjSize: {}, ManifsetSize: {}, ManifestHeadSize: {}, ManifestHeadMax: {},".format(name, size_actual, size_accounted, size_diff))
print(tabulate(rows, headers))


