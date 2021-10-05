#! /bin/bash

echo "Deleting all objects and bucket in test-bucket"
cd /root/source/ceph/build
./bin/radosgw-admin bucket rm --bucket test-bucket --purge-objects

echo "Running GC now...."
./bin/radosgw-admin gc process --include-all

echo "Creating test-bucket again"
cd /root/ceph_scripts
./create_bucket.sh
