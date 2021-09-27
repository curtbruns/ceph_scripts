#! /bin/bash

cd /root/source/ceph/build
./bin/ceph config set osd  bluestore_min_alloc_size_ssd 65536
