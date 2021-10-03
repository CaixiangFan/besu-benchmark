#!/bin/bash
rm /etc/machine-id
systemd-machine-id-setup
cd /home/ubuntu
sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/deploy
sudo -H -u ubuntu bash -c 'python3 deploy.py 192.168.23.64 40'
