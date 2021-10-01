#!bin/bash
# docker stop $(docker ps -q)
# sleep 3
export HOSTNAME=$(hostname)
# export DIR=$(pwd)
docker run --rm \
    --name $HOSTNAME \
    --net host \
    -v ${PWD}/data:/opt/besu/data \
    -v ${PWD}/../genesis.json:/config/genesis.json \
    -v ${PWD}/config.toml:/config/config.toml \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml