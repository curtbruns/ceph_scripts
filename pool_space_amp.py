import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')

def get_erasure_extras(pool):
    running_size = 0
    #print("Checking stat of objects in pool: {}".format(pool))
    cmd_stat = subprocess.run(["./bin/rados", "-p", pool, "ls"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    #print("Cmd_stat stdout: {}".format(cmd_stat.stdout))
    object_list = cmd_stat.stdout.replace(" ", "").split("\n")
    #print("{} Objects in List: {}, pool: {}".format(len(object_list), object_list, pool))
    print("{} Objects to Review in pool: {}".format(len(object_list), pool))
    for obj in object_list:
        if len(obj) == 0:
            continue
        cmd_stat = subprocess.run(["./bin/rados", "-p", pool, "stat", obj], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        output = cmd_stat.stdout.strip()
        obj_data = output.split(", size")
        #print("Obj_data: {} and SIZE: {}".format(obj_data, obj_data[1]))
        running_size += int(obj_data[1])
    print("Total size of rados objects in pool: {} is: {}".format(pool, running_size))
    return int(running_size)

def calc_rep(pool, data):
    print("Calculating replicated data for pool: {} and stored data: {}".format(pool, data))
    #print("Replication Dict for this pool: {}".format(rep_dict[pool]))
    total_data = 0
    # Repl pool
    try: 
        total_data = data * rep_dict[pool]['replication']
        #print("Data with repl: {}".format(total_data))
    # Nope - it's an EC pool
    except KeyError:
        code_block_data = int((data / int(rep_dict[pool]['k'])) * (int(rep_dict[pool]['m'])))
        print("Code_block_data: {}, totalData: {}".format(code_block_data, data+code_block_data))
        total_data = data+code_block_data

    return total_data

# cebruns: TODO: Only doing this for buckets data - need to add Heads / Tails pools once I figure that out
# cebruns: TODO: What if it's an EC pool? 
POOLS=["default.rgw.buckets.data", "qlc_pool"]
ec_k = 0
ec_m = 0


rep_dict = dict()
# First get replication factor from pool info
# ./bin/ceph osd pool get default.rgw.buckets.index all -f json-pretty   # To get the "size" for replication and copies
for pool in POOLS:
    #print("Checking pool: {}".format(pool))
    ec_profile = ""
    replication = 0
    # Make sure pool exists
    cmd_stat = subprocess.run(["./bin/ceph", "osd", "pool", "ls", "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    pool_info = json.loads(cmd_stat.stdout)
    if pool not in pool_info:
        print("Pool: {} is NOT THERE".format(pool))
        #POOLS.remove(pool)
        continue
    cmd_stat = subprocess.run(["./bin/ceph", "osd", "pool", "get", pool, "all", "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    pool_stats = json.loads(cmd_stat.stdout)
    #print("Pool Stats: {}".format(pool_stats))
    try:
        ec_profile = pool_stats['erasure_code_profile'] 
        #print("{} is an erasure pool".format(pool))
        # Go get the k/m
        ec_cmd = subprocess.run(["./bin/ceph", "osd", "erasure-code-profile", "get", ec_profile,  "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        ec_info = json.loads(ec_cmd.stdout)
        ec_k = ec_info['k']
        ec_m = ec_info['m']
        # Go query the strip_size of the EC - osd_pool_erasure_code_stripe_unit
        # First get OSDs with qlc device-type
        qlc_cmd = subprocess.run(["./bin/ceph", "osd", "crush", "class", "ls-osd", "qlc", "-f", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        qlc_osds_info = json.loads(qlc_cmd.stdout)
        # Just check the first OSD
        osd_to_query = "osd." + str(qlc_osds_info[0]) 
        #print("Checking OSD: {}".format(osd_to_query))
        osd_cmd = subprocess.run(["./bin/ceph", "daemon", osd_to_query, "config", "get", "osd_pool_erasure_code_stripe_unit", "-f", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        osd_info = json.loads(osd_cmd.stdout)
        print("OSD: {}, has osd_pool_erasure_code_stripe_unit of: {}".format(osd_to_query, osd_info['osd_pool_erasure_code_stripe_unit']))
        osd_cmd = subprocess.run(["./bin/ceph", "daemon", osd_to_query, "config", "get", "bluestore_min_alloc_size_ssd", "-f", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        osd_alloc_info = json.loads(osd_cmd.stdout)
        print("OSD: {}, has bluestore_min_alloc_size_ssd of: {}".format(osd_to_query, osd_alloc_info['bluestore_min_alloc_size_ssd']))
    except KeyError:
        #print("{} is a replicated pool".format(pool))
        replication = pool_stats['size']
    #print("Replication found: {} for pool: {}".format(replication, pool))
    #print("Repl: {}".format(replication))
    if replication:
        rep_dict[pool] = dict({'replication': replication})
    else:
        rep_dict[pool] = dict({'k': ec_k, 'm': ec_m, 'stripe': osd_info['osd_pool_erasure_code_stripe_unit'] })

#print ("{}".format(rep_dict))

# Next get pool stats
#print ("our Rep_dict: {}".format(rep_dict))
cmd_stat = subprocess.run(["./bin/ceph", "df", "detail", "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
df_stats = json.loads(cmd_stat.stdout)
# Ceph has some expected SpaceAmp due to replication or EC - this is required for durability
# Ceph also can have space amp due to mismatch in alloc size and object size 
row = list()
for our_pool in POOLS:
    for pool in df_stats['pools']:
        if pool['name'] == our_pool:
            #print ("Pool info is: {}".format(pool))
            # Total Bytes used in Pool - includes replicas and alloc_size mismatches
            data_bytes_used = pool['stats']['data_bytes_used']
            # Stored object data 
            stored_data = pool['stats']['stored_data']
            # EC might have extra bytes if object stored is < stripe_width
            data_bytes_extra_for_erasure = stored_data - get_erasure_extras(our_pool) 
            #print("Stored data for pool: {} is: {}".format(our_pool, stored_data))
            # Calculate how much should be stored including replicas
#            stored_data_with_repl = pool['stats']['stored_data'] * replication
            stored_data_with_repl = calc_rep(pool['name'], pool['stats']['stored_data'])
            # Bytes added just due to replication or code blocks for EC
            space_amp_replication_bytes = stored_data_with_repl + data_bytes_extra_for_erasure - stored_data
            # Extra bytes that are not due to replication - due to alloc size
            size_diff_after_repl = data_bytes_used - stored_data_with_repl
            # Total bytes diff (includes repl and alloc overhead)
            total_bytes_diff = data_bytes_used - stored_data
            # Consider replication as space amp as well here
            if stored_data == 0:
                space_amp_replication_pct = "N/A"
                space_amp_due_to_alloc_pct = "N/A"
                space_amp_total_pct = "N/A"
            else: 
                space_amp_replication_pct = ("{:2.2%}".format(space_amp_replication_bytes / (stored_data - data_bytes_extra_for_erasure )))
                # e.g. 4197, single replication: 
                space_amp_due_to_alloc_pct = ("{:2.2%}".format((size_diff_after_repl / stored_data_with_repl)))
                space_amp_total_pct = ("{:2.2%}".format((data_bytes_used - stored_data) / stored_data))  # we subtract stored_data - it's our sunk cost of storing this data
                #space_amp_total_pct = ("{:2.2%}".format((data_bytes_used ) / stored_data)) 
            #print("Pool: {}, Objects: {}, Stored: {}, StoredWithRepl: {}, ActualBytesUsed: {}, SpaceAmp: {:2.2%}".format(pool['name'], pool['stats']['objects'], stored_data, stored_data_with_repl, data_bytes_used, float(space_amp)))
            key = pool['name']
            #print ("Rep_dict is: {}".format(rep_dict[(pool['name'])]))
            if "replication" in rep_dict[(pool['name'])]:
                repl_info = "(Repl: " + str(rep_dict[(pool['name'])]['replication']) + ")"
            else:
                repl_info = "(EC k: " + rep_dict[(pool['name'])]['k'] + " m: " + rep_dict[(pool['name'])]['m'] + ")"
            row.append([pool['name']+ repl_info, pool['stats']['objects'], stored_data, data_bytes_extra_for_erasure, stored_data_with_repl, space_amp_replication_bytes, space_amp_replication_pct, data_bytes_used, total_bytes_diff, size_diff_after_repl, space_amp_due_to_alloc_pct, space_amp_total_pct])
headers = ["Pool"                            ,         "RADOSObjects",       "Stored", "ExtraECBytes",             "ExpectedTotalWithRepl",  "SpaceAmpReplOnly",              "SpaceAmpRepl%",       "TotalStored",   "TotalBytesDiff", "ByteAmpDueToAllocSize", "SpaceAmpInPoolForAllocSize", "SpaceAmpTotal"]
print(tabulate(row, headers))

