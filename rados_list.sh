#! /bin/bash

cd /root/source/ceph/build

./bin/radosgw-admin bucket rados list --rgw-obj-fs ","
