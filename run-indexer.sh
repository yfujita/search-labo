#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
base_dir=$(pwd)

data_dir=$base_dir/output_20240616

cd $base_dir/indexer || exit

docker build -t search-labo/indexer:latest .
docker run \
    --rm \
    --network=search-labo_default \
    -v $data_dir:/data \
    search-labo/indexer:latest
