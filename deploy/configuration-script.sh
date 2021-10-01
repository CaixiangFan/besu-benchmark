sudo rm /etc/machine-id
sudo systemd-machine-id-setup
cd /home/ubuntu
git clone https://pat@github.com/CaixiangFan/bpet.git
cd bpet/deploy
python3 deploy.py
