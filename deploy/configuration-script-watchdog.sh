#!/bin/bash
rm /etc/machine-id
systemd-machine-id-setup
systemd-resolve --flush-caches
cd /home/ubuntu || exit

# SET UP watchdog as the NTP server
sudo apt update -y
sudo apt install ntp -y
# replace the default NTP pool servers with closest servers
sudo nano /etc/ntp.conf
# server 0.north-america.pool.ntp.org
# server 1.north-america.pool.ntp.org
# server 2.north-america.pool.ntp.org
# server 3.north-america.pool.ntp.org
sudo systemctl restart ntp

# install docker
cd /home/ubuntu || exit
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo groupadd docker
sudo usermod -aG docker ubuntu
newgrp docker

sudo -H -u ubuntu bash -c 'curl -fsSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py'
python3 get-pip.py
sudo -H -u ubuntu bash -c 'python3 -m pip install redis'