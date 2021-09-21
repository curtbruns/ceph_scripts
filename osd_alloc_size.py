import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')
#./bin/radosgw-admin bucket list --bucket test-bucket
osd_list = subprocess.run(["./bin/ceph", "osd", "df", "-f", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
osds = json.loads(osd_list.stdout)
rows = []
#print ("OSDs json: {}".format(osds))
headers = ["OSD-ID", "Class", "MinAllocSizeHDD", "MinAllocSizeSSD"]
for osd in osds['nodes']:
    #print ("Osd: {}".format(osd))
    osd_id = osd['id']
    osd_class = osd['device_class']
    osd_config = subprocess.run(["./bin/ceph", "daemon", "osd."+str(osd_id), "config", "show", "-f", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    osd_list = json.loads(osd_config.stdout)
    osd_min_alloc_ssd = osd_list['bluestore_min_alloc_size_ssd']
    osd_min_alloc_hdd = osd_list['bluestore_min_alloc_size_hdd']

    rows.append([osd_id, osd_class, osd_min_alloc_hdd, osd_min_alloc_ssd])
print('\n')
print(tabulate(rows, headers))

