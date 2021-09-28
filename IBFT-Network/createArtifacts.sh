export BESU_HOME=/home/ubuntu/IBFT-Network
docker run --rm -d \
    --name besu_config \
    -v $BESU_HOME/networkFiles:/opt/besu/networkFiles \
    -v $BESU_HOME/ibftConfigFile.json:/config/ibftConfigFile.json \
    hyperledger/besu:21.10 \
    operator generate-blockchain-config \
    --config-file=/config/ibftConfigFile.json \
    --to=/opt/besu/networkFiles \
    --private-key-file-name=key