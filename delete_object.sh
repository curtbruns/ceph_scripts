#! /bin/bash

if [ -z $1 ]; then
	echo "add key to delete on command-line"
	exit -1
fi
aws --profile=ceph --endpoint=http://localhost:8000 s3api delete-object --bucket test-bucket --key $1

