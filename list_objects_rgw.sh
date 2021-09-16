#! /bin/bash

cd /root/source/ceph/build
if [ -z $1 ]; then
	echo "using test-bucket"
	bucket=test-bucket
else
	bucket=$1
fi
#aws --profile=ceph --endpoint=http://localhost:8000 s3api list-objects --bucket=${bucket}
./bin/radosgw-admin bucket list --bucket ${bucket}

