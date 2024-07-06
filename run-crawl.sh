#!/bin/bash
set -e

cd "$(dirname "$0")" || exit
base_dir=$(pwd)

for OPT in "$@"; do
    case $OPT in
        -e | --env)
            env_name=$2
            shift 2
            ;;
        *)
            if [[ ! -z "$1" ]] && [[ ! "$1" =~ ^-+ ]]; then
                shift 1
            fi
            ;;
      esac
done

if [ -z "$env_name" ]; then
    echo "Please specify the output directory"
    exit 1
fi

if [ -e $base_dir/crawl-results/$env_name ]; then
    rm -rf "$base_dir/crawl-results/$env_name"
fi
mkdir -p "$base_dir/crawl-results/$env_name"

cd $base_dir/crawler-web || exit

docker build -t crawler-web-test:latest .
docker run --rm -v $base_dir/crawl-results/$env_name:/output -e ENV=$env_name crawler-web-test:latest
