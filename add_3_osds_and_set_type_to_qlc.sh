#! /bin/bash

if [ -n $1 ]; then
	echo "Add erasure or replicated on command-line for qlc pool to create"
	exit -1
fi
POOL=$1
if [ $POOL != "replicated" ]; then
	if [ $POOL != "erasure" ]; then
		echo "Neither replicated nor erasure found in: $POOL"
		exit -1
	fi
fi


cd /root/source/ceph/build
../src/vstart.sh --inc-osd 3
echo "Adding OSDs"
if [ $? -ne 0 ]; then
	echo "Adding OSDs failed..."
	exit -1
fi

echo "Removing SSD class - assuming OSDs 3,4,5"
./bin/ceph osd crush rm-device-class osd.3 osd.4 osd.5
if [ $? -ne 0 ]; then
	echo "Failed to remove device class"
	exit -1
fi

echo "Adding QLC class - assuming OSDs 3,4,5"
./bin/ceph osd crush set-device-class qlc osd.3 osd.4 osd.5
if [ $? -ne 0 ]; then
	echo "Failed to set qlc device class"
	exit -1
fi

# must use OSD as the "crush bucket" because if you use Host (like you normally would) - you won't get any replication as all OSDs are on one host in vstart env
if [ $POOL == "replicated" ]; then
	echo "Creating QLC Crush Rule - replicated - use OSD as replicant bucket as all OSDs are on one host in vstart env"
	./bin/ceph osd crush rule create-replicated qlc_rule default osd qlc
	if [ $? -ne 0 ]; then
		echo "Failed to set QLC crush rule"
		exit -1
	fi
	echo "Creating a REPLICATED Pool for QLC"
	./bin/ceph osd pool create qlc_pool replicated qlc_rule
	if [ $? -ne 0 ]; then
		echo "Failed to Create QLC Pool with qlc_rule"
		exit -1
	fi
else
	echo "Creating ERASURE QLC Rule for QLC Device Types"
	./bin/ceph osd erasure-code-profile set qlc_ec plugin=jerasure k=2 m=1 technique=reed_sol_van crush-failure-domain=osd crush-device-class=qlc
	if [ $? -ne 0 ]; then
		echo "Failed creating ERASURE pool"
		exit -1
	fi
	echo "Creating ERASURE Pool"
	./bin/ceph osd pool create qlc_pool erasure qlc_ec
	if [ $? -ne 0 ]; then
		echo "Failed to Create QLC Pool with qlc_ec rule"
		exit -1
	fi
fi

