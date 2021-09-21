#! /bin/bash

KEY=fiver
# only one
for i in {4..4}; do
	echo "Putting key of: ${KEY}-${i}"
	aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body ./512B_object.bin
done

