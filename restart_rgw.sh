#! /bin/bash

cd /root/source/ceph/build
echo Stopping RGW via src/stop.sh
../src/stop.sh rgw

echo Clear out log
echo "" > /root/source/ceph/build/out/radosgw.8000.log

sleep 2
echo Restarting RGW
/root/source/ceph/build/bin/radosgw -c /root/source/ceph/build/ceph.conf --log-file=/root/source/ceph/build/out/radosgw.8000.log --admin-socket=/root/source/ceph/build/out/radosgw.8000.asok --pid-file=/root/source/ceph/build/out/radosgw.8000.pid --rgw_luarocks_location=/root/source/ceph/build/out/luarocks --debug-rgw=20 --debug-ms=1 -n client.rgw.8000 '--rgw_frontends=beast port=8000'
