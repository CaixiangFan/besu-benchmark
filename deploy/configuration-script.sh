#!/bin/bash
rm /etc/machine-id
systemd-machine-id-setup
systemd-resolve --flush-caches
cd /home/ubuntu || exit

sudo apt update -y
sudo apt install ntpdate -y
# add the NTP server’s IP address and hostname in the /etc/hosts file
echo '10.2.1.9	  watchdog' | sudo tee -a /etc/hosts
sudo timedatectl set-ntp off
# install NTP service on the client system
sudo apt install ntp -y
# Configure NTP Client
echo 'server watchdog prefer iburst' | sudo tee -a /etc/ntp.conf
sudo systemctl restart ntp

sudo -H -u ubuntu bash -c 'git clone https://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@github.com/CaixiangFan/bpet.git'
cd bpet/deploy || exit
sudo -H -u ubuntu bash -c 'python3 deploy.py 10.2.1.9 4'