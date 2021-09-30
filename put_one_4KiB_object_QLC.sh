#! /bin/bash

i=0
echo "Putting key of: asdf-${i}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key asdf-${i} --body ./4KiB_object.bin --storage-class QLC_CLASS

