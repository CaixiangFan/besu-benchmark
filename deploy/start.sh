#!/bin/bash
export HOSTNAME=$(hostname)
export BESU_OPTS='-Xmx16g -Xms8g'
docker run -d --rm \
    --name $HOSTNAME \
    --net host \
    -v ${PWD}/data:/opt/besu/data \
    -v ${PWD}/genesis.json:/config/genesis.json \
    -v ${PWD}/config.toml:/config/config.toml \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml

sleep 3

docker run --rm -d \
    --name pushgateway \
    -p 9091:9091 \
    prom/pushgateway