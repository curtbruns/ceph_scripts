#! /bin/bash

KEY=qwerty

for i in {0..9}; do
	echo "Putting key of: ${KEY}-${i}"
	aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key ${KEY}-${i} --body ./512B_object.bin
done

