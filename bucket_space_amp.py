import json
import sys
import subprocess
import os
os.chdir('/root/source/ceph/build')
bucket_stat = subprocess.run(["./bin/radosgw-admin", "bucket", "stats"], stdout=subprocess.PIPE, text=True)
buckets = json.loads(bucket_stat.stdout)
for bucket in buckets:
    size_actual =  bucket['usage']['rgw.main']['size_actual']
    size_util = bucket['usage']['rgw.main']['size_utilized']
    space_amp = (1-((size_util / size_actual)))
    print("Bucket: {}, Objects: {}, SizeUtil: {}, SizeActual: {}, BucketSpaceAmp: {:2.2%}".format(bucket['bucket'], bucket['usage']['rgw.main']['num_objects'], size_util, size_actual, float(space_amp)))
