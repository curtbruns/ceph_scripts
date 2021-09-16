#! /bin/bash

cd /root/source/ceph/build
./bin/ceph --admin-daemon ./out/radosgw.8000.asok config get debug_ms
