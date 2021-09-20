#! /bin/bash

cd /root/ceph_scripts
echo
echo "****** Object Trace ******"
python3 object_trace.py
echo 
echo "****** Bucket Amp ******"
python3 bucket_space_amp.py
echo 
echo "****** Pool Amp ******"
python3 pool_space_amp.py
