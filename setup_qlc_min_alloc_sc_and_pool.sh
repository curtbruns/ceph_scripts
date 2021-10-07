#! /bin/bash
BUILD_DIR=/root/source/ceph/build
SCRIPT_DIR=/root/ceph_scripts

check_fail() {
if [ $? -ne 0 ]; then
	echo "Failed"
	exit -1
fi
}

POOL=$1
#echo "Pool chosen: $POOL"

if [ -z "$POOL" ]; then
    echo "Add erasure or replicated on command-line for qlc pool to create"
    exit -1
fi

echo "Setup default.rgw.buckets.data to use replicated rule and ssd class"
cd $BUILD_DIR
./bin/ceph osd crush rule create-replicated rgw_rule default osd ssd
check_fail
echo "Putting one object to force the default rgw bucket to be created"
cd $SCRIPT_DIR
./put_one_4KiB_object.sh
cd $BUILD_DIR
echo "Now setting the bucket data to use rgw_rule for SSD class"
./bin/ceph osd pool set default.rgw.buckets.data crush_rule rgw_rule
check_fail
# Now delete the object rule and pool will stay in place
cd $SCRIPT_DIR
./clean_bucket.sh

echo "Setting Min Alloc to 64K before launching next OSDs"
cd $SCRIPT_DIR
./set_min_alloc.sh
check_fail

echo "Adding 3 OSDs and setting Device class to qlc"
./add_3_osds_and_set_type_to_qlc.sh $POOL
check_fail

echo "Creating QLC Storage Class for qlc_pool"
./create_QLC_sc.sh
check_fail

echo "Pushing the pre-req lua script"
./push_pre_req_sc.lua
check_fail
