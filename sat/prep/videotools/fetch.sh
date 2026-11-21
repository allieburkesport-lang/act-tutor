#!/bin/bash
# fetch.sh <lid> <date> idx:HHMMSS:jobid ...
lid=$1; dt=$2; shift 2; mkdir -p $lid
for x in "$@"; do IFS=: read i t j <<< "$x"; curl -sf -o $lid/scene_$i.mp3 "https://d8j0ntlcm91z4.cloudfront.net/user_3DUbBZiyejYyfdhJYyniXJ1ktTE/hf_${dt}_${t}_${j}.mp3" || echo "FAIL $i"; done
ls $lid | wc -l
