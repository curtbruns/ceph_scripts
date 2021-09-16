#! /bin/bash

if [ -z $1 ]; then
	echo "add key to put on command-line - 1st argument"
	exit -1
fi

if [ -z $2 ]; then
	echo "add object to put on commmand-line - 2nd argument"
	exit -2
fi
aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key $1 --body ./$2

