#!/bin/bash
export DEPLOYDIR=/home/ubuntu
export HOSTNAME=$(hostname)
mkdir ${DEPLOYDIR}/data
docker run -d --rm \
    --name $HOSTNAME \
    --net host \
    -v ${DEPLOYDIR}/data:/opt/besu/data \
    -v ${PWD}/genesis.json:/config/genesis.json \
    -v ${PWD}/config.toml:/config/config.toml \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml