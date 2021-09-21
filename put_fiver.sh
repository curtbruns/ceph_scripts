#! /bin/bash

KEY=fiver
if [ -z $1 ]; then
	echo "Add subkey (fiver-XX) for execution"
	exit -1
fi
SUBKEY=$1

# only one
echo "Putting key of: ${KEY}-${SUBKEY}"
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${SUBKEY} --body ./512B_object.bin

