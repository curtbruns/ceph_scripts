#! /bin/bash

#cd /root/source/ceph/build
#./bin/ceph daemon osd.2 config show | grep min_alloc

cd /root/ceph_scripts
echo "" > /root/source/ceph/build/out/mon.a.log
echo "" > /root/source/ceph/build/out/mon.b.log
echo "" > /root/source/ceph/build/out/mon.c.log
echo "" > /root/source/ceph/build/out/mgr.x.log
python ./osd_alloc_size.py
cp -f /root/source/ceph/build/out/mon.a.log /tmp/.
cp -f /root/source/ceph/build/out/mon.b.log /tmp/.
cp -f /root/source/ceph/build/out/mon.c.log /tmp/.
cp -f /root/source/ceph/build/out/mgr.x.log /tmp/.
