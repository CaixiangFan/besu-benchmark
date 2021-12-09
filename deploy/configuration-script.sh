#!/bin/bash
rm /etc/machine-id
systemd-machine-id-setup
systemd-resolve --flush-caches
cd /home/ubuntu || exit
sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/deploy || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 192.168.226.163 50'