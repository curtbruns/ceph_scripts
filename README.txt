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

# Change replication to 2 for data pool:
./bin/ceph osd pool default.rgw.buckets.data size 2
