#! /bin/bash

aws --profile=ceph --endpoint=http://localhost:8000 s3api put-object --bucket test-bucket --key tenMiB-1 --body ./10MiB_object.bin --storage-class QLC_CLASS

