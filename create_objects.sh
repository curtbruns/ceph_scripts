#! /bin/bash

# 4096 object
dd if=/dev/zero of=./4KiB_object.bin bs=4096 count=1

# 4097 object
dd if=/dev/zero of=./4097B_object.bin bs=4097 count=1

# 512B object
dd if=/dev/zero of=./512B_object.bin bs=512 count=1

# 10MiB object
dd if=/dev/zero of=./10MiB_object.bin bs=1M count=10

# 4MiB object
dd if=/dev/zero of=./10MiB_object.bin bs=4M count=1

# 64KiB object
dd if=/dev/zero of=./64KiB_object.bin bs=64K count=1

# 64KiB+1B object
dd if=/dev/zero of=./65537B_object.bin bs=65537 count=1
