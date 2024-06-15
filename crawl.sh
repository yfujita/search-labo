#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
base_dir=$(pwd)

if [ -e $base_dir/output ]; then
    rm -rf ./output
fi
mkdir $base_dir/output

cd $base_dir/crawler-web || exit

docker build -t crawler-web-test:latest .
docker run --rm -v $base_dir/output:/output crawler-web-test:latest
