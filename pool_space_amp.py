import json
import sys
import subprocess
import os
os.chdir('/root/source/ceph/build')

# First get replication factor from pool info
# ./bin/ceph osd pool get default.rgw.buckets.index all -f json-pretty   # To get the "size" for replication and copies
cmd_stat = subprocess.run(["./bin/ceph", "osd", "pool", "get", "default.rgw.buckets.index", "all", "-f", "json-pretty"], stdout=subprocess.PIPE, text=True)
pool_stats = json.loads(cmd_stat.stdout)
replication = pool_stats['size']
#print("Repl: {}".format(replication))

# Next get pool stats
cmd_stat = subprocess.run(["./bin/ceph", "df", "detail", "-f", "json-pretty"], stdout=subprocess.PIPE, text=True)
df_stats = json.loads(cmd_stat.stdout)
for pool in df_stats['pools']:
    if pool['name'] == "default.rgw.buckets.data":
        stored_data = pool['stats']['stored_data']
        stored_data_with_repl = pool['stats']['stored_data'] * replication
        data_bytes_used = pool['stats']['data_bytes_used']
        space_amp = (1-((stored_data_with_repl / data_bytes_used )))
        print("Pool: {}, Objects: {}, Stored: {}, StoredWithRepl: {}, ActualBytesUsed: {}, SpaceAmp: {:2.2%}".format(pool['name'], pool['stats']['objects'], stored_data, stored_data_with_repl, data_bytes_used, float(space_amp)))
