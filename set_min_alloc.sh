#! /bin/bash

cd /root/source/ceph/build
./bin/ceph config set osd  bluestore_min_alloc_size_ssd 65536
if [ $? -ne 0 ]; then
	echo "Failed to set min alloc to 64K"
	exit -1
fi
