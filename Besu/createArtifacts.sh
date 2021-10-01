#!/bin/bash

docker run --rm \
    --name besu_config \
    -v $(pwd)/networkFiles:/opt/besu/networkFiles \
    -v $(pwd)/ibftConfigFile.json:/config/ibftConfigFile.json \
    hyperledger/besu:21.10 \
    operator generate-blockchain-config \
    --config-file=/config/ibftConfigFile.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key

sleep 3


