import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')
bucket_stat = subprocess.run(["./bin/radosgw-admin", "bucket", "stats"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
buckets = json.loads(bucket_stat.stdout)
headers = ["Bucket", "Objects", "SizeUtil", "SizeActual", "Diff", "BucketSpaceAmp"]
for bucket in buckets:
    size_actual =  bucket['usage']['rgw.main']['size_actual']
    size_util = bucket['usage']['rgw.main']['size_utilized']
    size_diff =  size_actual - size_util
    space_amp = ("{:2.2%}".format((1-((size_util / size_actual)))))
#    print("Bucket: {}, Objects: {}, SizeUtil: {}, SizeActual: {}, BucketSpaceAmp: {:2.2%}".format(bucket['bucket'], bucket['usage']['rgw.main']['num_objects'], size_util, size_actual, float(space_amp)))
    row = [[bucket['bucket'], bucket['usage']['rgw.main']['num_objects'], size_util, size_actual, size_diff, space_amp]]
print(tabulate(row, headers))
