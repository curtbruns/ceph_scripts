#! /bin/bash

i=0
KEY=niner
echo "Putting key of: ${KEY}-${i}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body ./9MiB_object.bin

