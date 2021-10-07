#! /bin/bash

i=0
KEY=truv2
echo "Putting key of: ${KEY}-${i}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body /root/ceph_scripts/65537B_object.bin --storage-class STANDARD

