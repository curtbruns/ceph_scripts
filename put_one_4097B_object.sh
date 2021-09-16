#! /bin/bash

KEY=testing
# only one
for i in {0..0}; do
	echo "Putting key of: ${KEY}-${i}"
	aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body ./4097B_object.bin
done

