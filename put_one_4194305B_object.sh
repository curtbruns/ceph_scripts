#! /bin/bash

i=0
echo "Putting key of: biggee-${i}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key biggee-${i} --body ./4194305_object.bin

