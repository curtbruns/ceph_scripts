# Can also find objects pg/osd map and replication factor by how many OSDs:
./bin/ceph osd map default.rgw.buckets.data qwerty-0
Output:
# This doesn't really see that the object is there - it tells you where it WOULD Be through the crush map (I think) because you can give it a bogus object name and it still outputs
osdmap e282 pool 'default.rgw.buckets.data' (7) object 'qwerty-0' -> pg 7.4fe8a1fe (7.1e) -> up ([1,0,2], p1) acting ([1,0,2], p1)


# Map pgs by osd:
./bin/ceph pg ls-by-osd osd.0

# Get pg dump info:
./bin/ceph pg dump 

# Get PG list for a pool
# Note the first number is the pool id: 7.xx and xx is the PG number
./bin/ceph pg ls-by-pool ${BD}

# Change replication to 1 for data pool:
./bin/ceph osd pool set default.rgw.buckets.data size 1 --yes-i-really-mean-it
# Change replication to 2 for data pool:
./bin/ceph osd pool set default.rgw.buckets.data size 2

# Add an OSD to vstart cluster:
../src/vstart.sh --inc-osd

# Check OSD DF
./bin/ceph osd df class ssd

# Change ceph alloc size and then launch another OSD
./bin/ceph config set osd  bluestore_min_alloc_size_ssd 65536
../src/vstart.sh --inc-osd 1

# Check All OSDs min_alloc
python osd_alloc_size.py
# NOTE in the log files, the running OSDs will complain they can't change their min_alloc:
out/osd.0.log:2021-09-21T17:36:22.187-0400 7f78d9d5e640  4 set_mon_vals failed to set bluestore_min_alloc_size_ssd = 65536: Configuration option 'bluestore_min_alloc_size_ssd' may not be modified at runtime
out/osd.1.log:2021-09-21T17:36:22.183-0400 7f55d8b40640  4 set_mon_vals failed to set bluestore_min_alloc_size_ssd = 65536: Configuration option 'bluestore_min_alloc_size_ssd' may not be modified at runtime
out/osd.2.log:2021-09-21T17:36:22.184-0400 7fc532fa4640  4 set_mon_vals failed to set bluestore_min_alloc_size_ssd = 65536: Configuration option 'bluestore_min_alloc_size_ssd' may not be modified at runtime
# But this last one was created after change was made to the cluster
out/osd.3.log:2021-09-21T17:49:26.767-0400 7f7392794640 20 set_mon_vals bluestore_min_alloc_size_ssd = 65536 (no change)

# Crazy Mapping of S3 -> RADOS objects causes harm with the osd map tool to find out what osd it is being mapped to!
./bin/ceph osd map default.rgw.buckets.data 512B-0   # This works if you are going to use ./bin/rados put <object-name> <file-pat> --pool=<pool>
ce;./bin/ceph osd map default.rgw.buckets.data 512B-2
/root/source/ceph/build
*** DEVELOPER MODE: setting PATH, PYTHONPATH and LD_LIBRARY_PATH ***
2021-09-21T18:36:00.778-0400 7f7bb5491640 -1 WARNING: all dangerous and experimental features are enabled.
2021-09-21T18:36:00.804-0400 7f7bb5491640 -1 WARNING: all dangerous and experimental features are enabled.
osdmap e226 pool 'default.rgw.buckets.data' (7) object '512B-2' -> pg 7.947107a1 (7.1) -> up ([2], p2) acting ([2], p2)
# Says p2 and it is indeed p2 AFAIK
# ^^^^^ Does not work for the S3 object name that you do with the command line...

# Note that if you "PUT" an object with the rados command line, it will use your object-name as the object-name - cool, but that doesn't happen with RGW....
It uses the "bucket_id" as the prefix for the rados object name:
./bin/rados ls --pool ${BD}
512B-2  # Object I 'put' with the rados cli
478abffd-7977-4b31-a7f3-0c95b25e99e0.4353.5_fiver-0  # object I 'put' with the RGW interface
^^^^ You can find this ID with : ./bin/radosgw-admin bucket stats
^^^^ Watch bucket id changes to .5, .6, etc as you delete and then create a new test-bucket
./bin/ceph osd map ${BD} 478abffd-7977-4b31-a7f3-0c95b25e99e0.4353.6_fiver-1
OUTPUT: 
osdmap e226 pool 'default.rgw.buckets.data' (7) object '478abffd-7977-4b31-a7f3-0c95b25e99e0.4353.6_fiver-1' -> pg 7.d895e5c9 (7.9) -> up ([0], p0) acting ([0], p0)
BOOM.....

# Add device class of qlc
# Move osd to new device class
# Delete current class
./bin/ceph osd crush rm-device-class osd.2 osd.1
# Set new class
./bin/ceph osd crush set-device-class qlc osd.2 osd.1

# Crush replicated rule for qlc devices
./bin/ceph osd crush rule create-replicated qlc_rule default host qlc

# Trying to auto-set the device class:
in OSD section - this works and doesn't set device-class on new osds
        ; cebruns
        ;osd_class_update_on_start = false

in OSD section, this does not work:
        ; cebruns did not work
        ;class:qlc4
		and neither did crush_device_class:qlc4



# Storage Targets and Placement stuff:
./bin/radosgw-admin zonegroup placement list
./bin/radosgw-admin zonegroup placement add --rgw-zonegroup default --placement-id default-placement --storage-class QLC_CLASS
./bin/radosgw-admin zonegroup placement list
[
    {
        "key": "default-placement",
        "val": {
            "name": "default-placement",
            "tags": [],
            "storage_classes": [
                "QLC_CLASS",
                "STANDARD"
            ]
        }
    }
]

./bin/radosgw-admin zone placement  list
[
    {
        "key": "default-placement",
        "val": {
            "index_pool": "default.rgw.buckets.index",
            "storage_classes": {
                "STANDARD": {
                    "data_pool": "default.rgw.buckets.data"
                }
            },
            "data_extra_pool": "default.rgw.buckets.non-ec",
            "index_type": 0
        }
    }
]

# Point the GLACIER SC to the qlc_pool:
./bin/radosgw-admin zone placement add --rgw-zone default --placement-id default-placement --storage-class GLACIER --data-pool qlc_pool

# Using the S3API, we have these SCs available:
Possible values:
STANDARD
REDUCED_REDUNDANCY
STANDARD_IA
ONEZONE_IA
INTELLIGENT_TIERING
GLACIER
DEEP_ARCHIVE
OUTPOSTS

# Buckets -> Placement Targets
# Create new placement-id 'newbie' to zonegroup:
./bin/radosgw-admin zonegroup placement add --rgw-zonegroup default --placement-id newbie
# Add info to zone
radosgw-admin zone placement add  --rgw-zone default  --placement-id newbie --data-pool default.rgw.buckets.data  --index-pool default.rgw.buckets.index  --data-extra-pool default.rgw.buckets.non-ec
# Add new SC to zonegroup:
radosgw-admin zonegroup placement add  --rgw-zonegroup default  --placement-id newbie --storage-class GLACIER
# Add SC to zone info:
radosgw-admin zone placement add  --rgw-zone default  --placement-id newbie --storage-class GLACIER  --data-pool default.rgw.buckets.data

# NOW WE HAVE TO RESTART OUR RGW!!
../src/stop.sh rgw


# Setup Erasure Coded pool for QLC device class
To create a new jerasure erasure code profile:

ceph osd erasure-code-profile set {name} \
     plugin=jerasure \
     k={data-chunks} \
     m={coding-chunks} \
     technique={reed_sol_van|reed_sol_r6_op|cauchy_orig|cauchy_good|liberation|blaum_roth|liber8tion} \
     [crush-root={root}] \
     [crush-failure-domain={bucket-type}] \
     [crush-device-class={device-class}] \
     [directory={directory}] \
     [--force]

# Decodes to:
# Decodes to:
./bin/ceph osd erasure-code-profile set qlc_ec plugin=jerasure k=2 m=1 technique=reed_sol_van crush-failure-domain=osd crush-device-class=qlc
