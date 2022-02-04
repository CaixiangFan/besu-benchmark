#!/bin/bash
# ON WATCHDOG Node: manually Set up watch-dog as the NTP server
sudo apt update -y
sudo apt install ntp -y
# replace the default NTP pool servers with closest servers
sudo nano /etc/ntp.conf
# server 0.north-america.pool.ntp.org
# server 1.north-america.pool.ntp.org
# server 2.north-america.pool.ntp.org
# server 3.north-america.pool.ntp.org
sudo systemctl restart ntp

# ON OTHER BESU NODES
# For all besu nodes, SET UP NTP CLIENT CONNECT TO NTP SERVER
sudo apt update -y
sudo apt install ntpdate -y
# add the NTP server’s IP address and hostname in the /etc/hosts file
echo '10.2.1.9	  watchdog' | sudo tee -a /etc/hosts
# manually verify the client system is in sync with the NTP server’s time
# sudo ntpdate watchdog
sudo timedatectl set-ntp off
# install NTP service on the client system
sudo apt install ntp -y
# Configure NTP Client
echo 'server watchdog prefer iburst' | sudo tee -a /etc/ntp.conf
sudo systemctl restart ntp
# verify sychronized successfully
# ntpq -p