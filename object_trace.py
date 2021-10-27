import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')
#./bin/radosgw-admin bucket list --bucket test-bucket
object_list = subprocess.run(["./bin/radosgw-admin", "bucket", "list", "--bucket", "test-bucket"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
placement_list = list()
objects = json.loads(object_list.stdout)
rows = []
headers = ["Name", "Size", "AccountedSize", "Diff", "ObjSize", "ManifestSize", "ManifestHeadSize", "ManifestHeadMax", "BucketHead", "BucketTails", "PlacementRule", "BeginStripeSize", "BeginCurStripe", "EndStripeSize", "EndCurStripe", "TotalRadosObjects"]
total_manifest_size = 0
total_rados_objects = 0
for object in objects:
    name = object['name']
    # Clear line and carriage return
    sys.stdout.write('\x1b[2K\r')
    sys.stdout.write('Tracing: ')
    sys.stdout.write(name)
    sys.stdout.flush()
    size_actual =  object['meta']['size']
    size_accounted =  object['meta']['accounted_size']
    size_diff = size_accounted - size_actual
    object_stat = subprocess.run(["./bin/radosgw-admin", "object", "stat", "--bucket", "test-bucket", "--object", name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8', errors='replace')
#    object_stat.stdout = unicode(object_stat.stdout, errors='replace')
    stats = json.loads(object_stat.stdout)
    size_obj = stats['size']
    size_man = stats['manifest']['obj_size']
    size_head_man = stats['manifest']['head_size']
    size_head_man_max = stats['manifest']['max_head_size']
    pool_tail_objects = stats['manifest']['tail_placement']['bucket']['name']
    pool_head_object  = stats['manifest']['begin_iter']['location']['obj']['bucket']['name']
    placement_rule    = stats['manifest']['begin_iter']['location']['placement_rule']
    placement_list.append(placement_rule)
    begin_stripe_size = stats['manifest']['begin_iter']['stripe_size']
    begin_cur_stripe = stats['manifest']['begin_iter']['cur_stripe']
    end_stripe_size = stats['manifest']['end_iter']['stripe_size']
    end_cur_stripe = stats['manifest']['end_iter']['cur_stripe']
    key_for_rados = stats['manifest']['end_iter']['location']['obj']['key']['name']
    namespace_rados = stats['manifest']['end_iter']['location']['obj']['key']['ns']
    bucket_id_rados  = stats['manifest']['end_iter']['location']['obj']['bucket']['bucket_id']
    #print("Key for rados: {} and Bucket id: {}, namespace: {}".format(key_for_rados, bucket_id_rados, namespace_rados))
#    sys.exit(0)
    namespace_rados = stats['manifest']['end_iter']['location']['obj']['key']['ns']
    total_objects = end_cur_stripe+1
    total_rados_objects += total_objects
    total_manifest_size += size_man
    rows.append([name, size_actual, size_accounted, size_diff, size_obj, size_man, size_head_man, size_head_man_max, pool_head_object, pool_tail_objects, placement_rule, begin_stripe_size, begin_cur_stripe, end_stripe_size, end_cur_stripe, total_objects])
    #print(name, size_actual, size_accounted, size_diff, size_obj, size_man, size_head_man, size_head_man_max, begin_stripe_size, begin_cur_stripe, end_stripe_size, end_cur_stripe)
    #print("Name: {}, Size: {}, AccountedSize: {}, Diff: {}, ObjSize: {}, ManifsetSize: {}, ManifestHeadSize: {}, ManifestHeadMax: {},".format(name, size_actual, size_accounted, size_diff))
print('\n')
print(tabulate(rows, headers))
headers = ['TotalRADOSObjects', 'TotalManifest']
rows = [[total_rados_objects, total_manifest_size]]
print(tabulate(rows, headers))

rows = []
# Add our STANDARD class to find it in placement list
placement_list.append('default-placement/STANDARD')
#print("placement_list: {}".format(placement_list))

for pr in placement_list:
#    print("Placement_Rule: {}".format(pr))
    if pr.find("/") != -1:
        storage_class = pr.split('default-placement/')[1]
    else:
        continue
#    print("Checking rule:  {} and SC: {}".format(pr, storage_class))
    sc_pool = subprocess.run(["./bin/radosgw-admin", "zone", "placement", "list"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    stats = json.loads(sc_pool.stdout)
#    print("Stats is: {}".format(stats))
    storage_class_pool = stats[0]['val']['storage_classes'][storage_class]['data_pool']
    rows.append([storage_class, storage_class_pool])
#    rows = [['STANDARD', standard_pool], [storage_class, storage_class_pool]]

headers = ['StorageClass', 'DataPool']
print(tabulate(rows, headers))
