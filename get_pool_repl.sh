#! /bin/bash

./bin/ceph osd pool get default.rgw.buckets.index all -f json-pretty

./bin/ceph osd pool get default.rgw.buckets.index all -f json-pretty | grep \"size\"
