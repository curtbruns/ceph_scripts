#! /bin/bash

aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key asdf --body ./new.bin

