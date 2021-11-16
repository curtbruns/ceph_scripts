#! /bin/bash

cd /root/source/ceph/build
# Zonegroup Classes
./bin/radosgw-admin zonegroup placement list

# Zonegroup Classes
./bin/radosgw-admin zone placement list
