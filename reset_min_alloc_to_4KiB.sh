#! /bin/bash

cd /root/source/ceph/build
echo "" > /root/source/ceph/build/out/mon.a.log
echo "" > /root/source/ceph/build/out/mon.b.log
echo "" > /root/source/ceph/build/out/mon.c.log
echo "" > /root/source/ceph/build/out/mgr.x.log
./bin/ceph config set osd  bluestore_min_alloc_size_ssd 4096
cp -f /root/source/ceph/build/out/mon.a.log /tmp/.
cp -f /root/source/ceph/build/out/mon.b.log /tmp/.
cp -f /root/source/ceph/build/out/mon.c.log /tmp/.
cp -f /root/source/ceph/build/out/mgr.x.log /tmp/.
if [ $? -ne 0 ]; then
	echo "Failed to set min alloc to 64K"
	exit -1
fi
