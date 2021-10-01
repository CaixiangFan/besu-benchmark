import re
from redis import Redis
import subprocess
import toml
import socket
import time

WATCHDOG_ADDRESS = "192.168.23.64"

hostname = socket.gethostname()
host_ip = socket.gethostbyname(socket.gethostname())

with open('config-template.toml', 'r') as f:
    config = toml.load(f)

config['identity'] = hostname
config['p2p-host'] = host_ip
config['rpc-http-host'] = host_ip
config['rpc-ws-host'] = host_ip
config['metrics-push-host'] = host_ip

redis_miscellaneous = Redis(host=WATCHDOG_ADDRESS, port=6379, db=0)
redis_hosts = Redis(host=WATCHDOG_ADDRESS, port=6379, db=1)
redis_enode = Redis(host=WATCHDOG_ADDRESS, port=6379, db=2)
redis_deployment_logs = Redis(host=WATCHDOG_ADDRESS, port=6379, db=3)

redis_hosts.set(host_ip, hostname)

try:
    is_master = redis_enode.setnx("master", host_ip)
    if is_master:
        with open('config.toml', 'w') as f:
            toml.dump(config, f)
        container_id = subprocess.run(['sh', 'start.sh'], stdout=subprocess.PIPE)
        container_id = container_id.stdout.decode().replace('\n', '')
        time.sleep(15)
        container_logs = subprocess.run(['docker', 'logs', container_id], stdout=subprocess.PIPE)
        container_logs = container_logs.stdout.decode()
        enode_url = re.findall(r"(enode?://[^\s]+)", container_logs)[0]
        redis_enode.set("enode", enode_url)
        redis_deployment_logs.set(host_ip, container_logs)
    else:
        time.sleep(30)
        enode_url = None
        while enode_url is None:
            redis_enode.get("enode").decode()
            time.sleep(5)
        config['bootnodes'] = f"""["{enode_url}"]"""
        with open('config.toml', 'w') as f:
            toml.dump(config, f)
        container_id = subprocess.run(['sh', 'start.sh'], stdout=subprocess.PIPE)
        container_id = container_id.stdout.decode().replace('\n', '')
        time.sleep(15)
        container_logs = subprocess.run(['docker', 'logs', container_id], stdout=subprocess.PIPE)
        container_logs = container_logs.stdout.decode()
        redis_deployment_logs.set(host_ip, container_logs)

except Exception as e:
    redis_deployment_logs.set(host_ip, str(e))
