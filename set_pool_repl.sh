#! /bin/bash

cd /root/source/ceph/build
if [ -z $1 ]; then
	echo "Must put replication factor on command-line (1, 2, or 3)"
	exit -1
fi
./bin/ceph osd pool set default.rgw.buckets.data size $1 --yes-i-really-mean-it
./bin/ceph osd pool get default.rgw.buckets.data all -f json-pretty | grep \"size\"
