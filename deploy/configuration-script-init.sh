#!/bin/bash
# install docker
cd /home/ubuntu || exit
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo groupadd docker
sudo usermod -aG docker ubuntu
newgrp docker

docker pull hyperledger/besu:21.10
sudo -H -u ubuntu bash -c 'curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
python3 get-pip.py
sudo -H -u ubuntu bash -c 'pip install redis'
sudo -H -u ubuntu bash -c 'pip install toml'
# enable docker remote API 
sudo sed -i '/ExecStart/s/$/ -H=tcp:\/\/0.0.0.0:2375/' /lib/systemd/system/docker.service
sudo systemctl daemon-reload
sudo service docker restart
sudo apt install iftop
sudo -H -u ubuntu bash -c 'git clone https://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0@github.com/CaixiangFan/bpet.git'
cd bpet/deploy || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 192.168.23.64 6'