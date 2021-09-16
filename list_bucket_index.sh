#! /bin/bash

cd /root/source/ceph/build

./bin/rados -p default.rgw.buckets.index ls
