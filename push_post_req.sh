#! /bin/bash

cd /root/source/ceph/build
./bin/radosgw-admin script put --context postRequest --infile /root/ceph_scripts/post-req.lua
if [ $? -ne 0 ]; then
	echo "Error pushing script"
	exit -1
fi
