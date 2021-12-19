#!/bin/bash
docker run -d --rm \
    --name $1 \
    --network besu-network \
    -v ${PWD}/data:/opt/besu/data \
    -v ${PWD}/../genesis.json:/config/genesis.json \
    -v ${PWD}/config.toml:/config/config.toml \
    -p $2:$2 \
    -p $3:$3 \
    -p $4:$4 \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml