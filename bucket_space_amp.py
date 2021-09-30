import json
import sys
import subprocess
import os
from tabulate import tabulate
os.chdir('/root/source/ceph/build')
bucket_stat = subprocess.run(["./bin/radosgw-admin", "bucket", "stats"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
buckets = json.loads(bucket_stat.stdout)
headers = ["Bucket", "RGWObjects", "SizeUtil", "SizeActual", "Diff", "BucketSpaceAmp"]
if (len(buckets) == 0):
    print("Must make the test_bucket first")
    sys.exit(-1)

for bucket in buckets:
    if 'rgw.main' in bucket['usage']:
        size_actual =  bucket['usage']['rgw.main']['size_actual']
        size_util = bucket['usage']['rgw.main']['size_utilized']
        size_diff =  size_actual - size_util
        # Let's say 4096 object, but 8192 stored...amp should be 100%: (size_actual - size_object) / size_object == 8192-4096 / 4096 == 1
    #    space_amp = ("{:2.2%}".format((1-((size_util / size_actual)))))
        space_amp = ("{:2.2%}".format((size_actual - size_util) / size_util))
    #    print("Bucket: {}, Objects: {}, SizeUtil: {}, SizeActual: {}, BucketSpaceAmp: {:2.2%}".format(bucket['bucket'], bucket['usage']['rgw.main']['num_objects'], size_util, size_actual, float(space_amp)))
        row = [[bucket['bucket'], bucket['usage']['rgw.main']['num_objects'], size_util, size_actual, size_diff, space_amp]]
    else:
        print("test-bucket has no data in it!")
        sys.exit(0)
print(tabulate(row, headers))
