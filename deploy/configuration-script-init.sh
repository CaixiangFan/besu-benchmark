#!/bin/bash
cd /home/ubuntu || exit
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker ubuntu
docker pull hyperledger/besu:21.10
sudo -H -u ubuntu bash -c 'curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
python3 get-pip.py
sudo -H -u ubuntu bash -c 'pip install redis'
sudo -H -u ubuntu bash -c 'pip install toml'
sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/deploy || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 192.168.23.64 6'