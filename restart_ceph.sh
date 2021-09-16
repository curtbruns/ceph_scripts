#! /bin/bash

#unset HTTPS_PROXY
#unset https_proxy
#unset HTTP_PROXY
#unset http_proxy
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

echo "Starting vstart.sh"
MDS=0 RGW=1 ../src/vstart.sh -d -n -x --bluestore 
#MDS=0 RGW=1 ../src/vstart.sh -d -n -x --localhost --bluestore  # works
#MDS=0 RGW=1 ../src/vstart.sh -d -n -x --localhost --bluestore --without-dashboard # works
#../src/vstart.sh --debug --new -x --localhost --bluestore
#RGW=1 ../src/vstart.sh -d -n -x 
if [ $? -ne 0 ]; then
	echo "Did not start correctly - check it"
	exit -1
fi

echo "Test User"
./bin/radosgw-admin  user info --uid testid

echo "Done!  Get to hacking..."
exit 0
