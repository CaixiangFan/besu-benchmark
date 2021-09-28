export BESU_HOME=/home/ubuntu/IBFT-Network
docker stop node1
sleep 3
docker run --rm -d \
    --name node1 \
    --net host \
    -v $BESU_HOME/Node-1/data:/opt/besu/data \
    -v $BESU_HOME/Node-1/data:/opt/besu/keys \
    -v $BESU_HOME/Node-1/data:/opt/besu/public-keys \
    -v $BESU_HOME/genesis.json:/config/genesis.json \
    -v $BESU_HOME/Node-1/config.toml:/config/config.toml \
    hyperledger/besu:21.10 \
    --config-file=/config/config.toml