#! /bin/bash

echo "Running GC now...."
cd /root/source/ceph/build
./bin/radosgw-admin gc process --include-all
