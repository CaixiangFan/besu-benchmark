#!/bin/bash
rm /etc/machine-id
systemd-machine-id-setup
systemd-resolve --flush-caches
cd /home/ubuntu || exit
sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/deploy || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 192.168.226.176 4'