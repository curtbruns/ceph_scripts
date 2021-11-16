#! /bin/bash

cd /root/source/ceph/build
#./bin/ceph config set osd  bluestore_min_alloc_size_ssd 65536
./bin/ceph config set osd bluestore_use_optimal_io_size_for_min_alloc_size true
if [ $? -ne 0 ]; then
	echo "Failed to set use_optimal bool to true"
	exit -1
fi
