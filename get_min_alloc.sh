#! /bin/bash

#cd /root/source/ceph/build
#./bin/ceph daemon osd.2 config show | grep min_alloc

cd /root/ceph_scripts
python ./osd_alloc_size.py
