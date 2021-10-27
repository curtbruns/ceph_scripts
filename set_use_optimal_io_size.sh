#! /bin/bash

cd /root/source/ceph/build
./bin/ceph config set osd  bluestore_use_optimal_io_size_for_min_alloc_size true
if [ $? -ne 0 ]; then
	echo "Failed to set bluestore_use_optimal_io_size"
	exit -1
fi
