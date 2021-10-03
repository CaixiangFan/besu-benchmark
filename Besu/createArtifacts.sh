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

sleep 10

if [ ! -d "nodes" ] 
then
    echo "Message: nodes directory does not exists."
    cp -r networkFiles nodes
else
    echo "Message: nodes directory exists."
fi

cd nodes/keys
array=(*)
len=${#array[@]}

i=1
for dir in "${array[@]}"; do 
 cd $dir && mkdir data && mv key* data/ && cd ..;
 mv $dir "node${i}" && echo "${dir}" > node${i}/address.txt && i=$((i+1));
done

mv * ../ && cd .. && rm -r keys;
echo "$len nodes artifacts created!"


