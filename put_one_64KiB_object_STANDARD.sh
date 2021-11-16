#! /bin/bash

i=0
KEY=truv
echo "Putting key of: ${KEY}-${i}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body ./64KiB_object.bin --storage-class STANDARD

