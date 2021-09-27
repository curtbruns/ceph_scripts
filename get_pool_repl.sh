#! /bin/bash

cd /root/source/ceph/build
./bin/ceph osd pool get default.rgw.buckets.data all -f json-pretty
./bin/ceph osd pool get default.rgw.buckets.data all -f json-pretty | grep \"size\"
