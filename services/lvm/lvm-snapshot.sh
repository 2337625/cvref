#!/bin/bash
name=$1
path=$2
lvcreate --name ${name}-snap --snapshot -L1024 /dev/${path}/${name}
