#!/bin/bash
name=$1
path=$2
lvconvert --merge /dev/${path}/${name}
