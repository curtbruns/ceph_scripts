#! /bin/bash

aws --profile=ceph --endpoint=http://localhost:8000 s3api delete-bucket --bucket test-bucket
