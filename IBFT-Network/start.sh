#!/bin/bash
docker run -d --rm \
    --name $1 \
    --net host \
    -v ${PWD}/data:/opt/besu/data \
    -v ${PWD}/genesis.json:/config/genesis.json \
    -v ${PWD}/config.toml:/config/config.toml \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml