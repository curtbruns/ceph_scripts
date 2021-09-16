#! /bin/bash

cd /root/source/ceph/build
if [ -z $1 ]; then
	echo "Use object (key) as the argument"
	exit -1
fi
./bin/radosgw-admin object stat --bucket test-bucket --object $1
