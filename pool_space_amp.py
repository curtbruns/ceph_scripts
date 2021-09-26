import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')

# cebruns: TODO: Only doing this for buckets data - need to add Heads / Tails pools once I figure that out
# cebruns: TODO: What if it's an EC pool? 
POOL="default.rgw.buckets.data"

# First get replication factor from pool info
# ./bin/ceph osd pool get default.rgw.buckets.index all -f json-pretty   # To get the "size" for replication and copies
cmd_stat = subprocess.run(["./bin/ceph", "osd", "pool", "get", POOL, "all", "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
pool_stats = json.loads(cmd_stat.stdout)
#print("Pool Stats: {}".format(pool_stats))
replication = pool_stats['size']
#print("Replication found: {}".format(replication))
#print("Repl: {}".format(replication))

# Next get pool stats
cmd_stat = subprocess.run(["./bin/ceph", "df", "detail", "-f", "json-pretty"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
df_stats = json.loads(cmd_stat.stdout)
# Ceph has some expected SpaceAmp due to replication or EC - this is required for durability
# Ceph also can have space amp due to mismatch in alloc size and object size 
for pool in df_stats['pools']:
    if pool['name'] == POOL:
        # Total Bytes used in Pool - includes replicas and alloc_size mismatches
        data_bytes_used = pool['stats']['data_bytes_used']
        # Stored object data 
        stored_data = pool['stats']['stored_data']
        # Calculate how much should be stored including replicas
        stored_data_with_repl = pool['stats']['stored_data'] * replication
        # Bytes added just due to replication 
        space_amp_replication_bytes = stored_data_with_repl - stored_data
        # Extra bytes that are not due to replication - due to alloc size
        size_diff_after_repl = data_bytes_used - stored_data_with_repl
        # Total bytes diff (includes repl and alloc overhead)
        total_bytes_diff = data_bytes_used - stored_data
        # Consider replication as space amp as well here
        space_amp_replication_pct = ("{:2.2%}".format(space_amp_replication_bytes / stored_data))
        # e.g. 4197, single replication: 
        space_amp_due_to_alloc_pct = ("{:2.2%}".format((stored_data_with_repl - stored_data) / stored_data))
        space_amp_total_pct = ("{:2.2%}".format((data_bytes_used - stored_data) / stored_data)) 
        #print("Pool: {}, Objects: {}, Stored: {}, StoredWithRepl: {}, ActualBytesUsed: {}, SpaceAmp: {:2.2%}".format(pool['name'], pool['stats']['objects'], stored_data, stored_data_with_repl, data_bytes_used, float(space_amp)))
        row = [[pool['name']+ " (Repl: " + str(replication) + ")", pool['stats']['objects'], stored_data, stored_data_with_repl, space_amp_replication_bytes, space_amp_replication_pct, data_bytes_used, total_bytes_diff, size_diff_after_repl, space_amp_due_to_alloc_pct, space_amp_total_pct]]
headers = ["Pool",         "Objects",     "Stored", "ExpectedTotalWithRepl",  "SpaceAmpReplOnly",              "SpaceAmpRepl%",          "TotalStored",     "TotalBytesDiff", "ByteAmpDueToAllocSize", "SpaceAmpInPoolForAllocSize", "SpaceAmpTotal"]
print(tabulate(row, headers))
