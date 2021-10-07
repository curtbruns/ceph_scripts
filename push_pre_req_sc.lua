#! /bin/bash

cd /root/source/ceph/build
./bin/radosgw-admin script put --context preRequest --infile /root/ceph_scripts/pre-req-add-sc.lua
if [ $? -ne 0 ]; then
	echo "Error pushing script"
	exit -1
fi
