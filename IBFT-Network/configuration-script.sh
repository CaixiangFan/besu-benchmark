#!/bin/bash
# echo "{\"ipv6\": true, \"fixed-cidr-v6\": \"2001:db8:abc1::/64\"}" > /etc/docker/daemon.json
# docker network create --subnet="2001:db8:abc1::/64" \
#     --gateway="2001:db8:abc1::1" \
#     --ipv6 \
#     besu-network \
cd /home/ubuntu || exit
sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/IBFT-Network || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 4'