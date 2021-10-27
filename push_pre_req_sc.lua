#! /bin/bash

cd /root/source/ceph/build
./bin/radosgw-admin script put --context preRequest --infile /root/ceph_scripts/storage_class.lua
if [ $? -ne 0 ]; then
	echo "Error pushing script"
	exit -1
fi
