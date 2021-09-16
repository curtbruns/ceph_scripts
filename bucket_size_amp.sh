#!/bin/bash

# Using vstart env in /root/source/ceph/build
cd /root/source/ceph/build

for B in $(./bin/radosgw-admin bucket list|python -c "import json,sys; [sys.stdout.write(bucket + '\n') for bucket in json.load(sys.stdin)]"); do
    STATS=$(./bin/radosgw-admin bucket stats --bucket=${B})
    SIZE_ACTUAL=$(echo $STATS|python -c 'import sys, json; print(json.load(sys.stdin)["usage"]["rgw.main"]["size"])')
    SIZE=$(echo $STATS|python -c 'import sys, json; print(json.load(sys.stdin)["usage"]["rgw.main"]["size_actual"])')
    BUCKET_AMP=$(echo $STATS|python -c 'import sys, json; Print(json.load(sys.stdin)["usage"]["rgw.main"]["size_actual"])')

    if [ "$?" -ne 0 ]; then
        continue
    fi

    echo "Bucket: $B Size: $SIZE, SizeActual: $SIZE_ACTUAL"

done
