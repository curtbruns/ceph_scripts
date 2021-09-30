#! /bin/bash

cd /root/source/ceph/build
# First create zonegroup placement into
./bin/radosgw-admin zonegroup placement add --rgw-zonegroup default --placement-id default-placement --storage-class QLC_CLASS
# Now point it at the qlc_pool:
./bin/radosgw-admin zone placement add --rgw-zone default --placement-id default-placement --storage-class QLC_CLASS --data-pool qlc_pool


echo "MUST RESTART RGW NOW"
echo "MUST RESTART RGW NOW"
echo "MUST RESTART RGW NOW"
echo "MUST RESTART RGW NOW"
