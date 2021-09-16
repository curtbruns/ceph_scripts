#! /bin/bash

echo "Stopping ceph cluster"
cd /root/source/ceph/build
../src/stop.sh

if [ $? -ne 0 ]; then
	echo "Did not stop correctly - check out what happened"
	exit -1
fi

echo "Removing out and dev directories for space"
rm -rf out dev
if [ $? -ne 0 ]; then
	echo "Did not remove correctly - check it"
	exit -1
fi

exit 0
