#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
base_dir=$(pwd)

for OPT in "$@"; do
    case $OPT in
        -e | --env)
            env=$2
            shift 2
            ;;
        *)
            if [[ ! -z "$1" ]] && [[ ! "$1" =~ ^-+ ]]; then
                shift 1
            fi
            ;;
      esac
done

if [ -z "$env" ]; then
    echo "Please specify the env"
    exit 1
fi

data_dir=$base_dir/crawl-results/$env

cd $base_dir/indexer || exit

docker build -t search-labo/indexer:latest .
docker run \
    --rm \
    --network=search-labo_default \
    -e ENV=$env \
    -v $data_dir:/data \
    search-labo/indexer:latest
