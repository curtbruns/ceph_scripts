#!/bin/bash
#
# Get the usage statistics of all RGW buckets
#
# Sort output with: ./rgw-bucket-stats.sh|sort -k 2 -n|tac
#
# Author: Wido den Hollander <wido@widodh.nl>
#

cd /root/source/ceph/build
for BUCKET in $(./bin/radosgw-admin bucket list|python -c "import json,sys; [sys.stdout.write(bucket + '\n') for bucket in json.load(sys.stdin)]"); do
    STATS=$(./bin/radosgw-admin bucket stats --bucket=$BUCKET)
    KB=$(echo $STATS|python -c 'import sys, json; print(json.load(sys.stdin)["usage"]["rgw.main"]["size_kb_actual"])')

    if [ "$?" -ne 0 ]; then
        continue
    fi

    echo "$BUCKET $KB"

done
