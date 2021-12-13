import yaml, subprocess, os, json, sys
from datetime import datetime

DEFAULT_IP = '192.168.226.64'
SEND_RATES = [50, 100, 150, 200, 250]
connection_url = "ws://" + DEFAULT_IP + ":8546"
if len(sys.argv) > 1:
    connection_url = "ws://" + sys.argv[1] + ":8546"
networkconfig = 'networks/4node-ibft2/networkconfig.json'
with open(networkconfig, 'r') as f:
    data = json.load(f)
    data['ethereum']['url'] = connection_url
with open(networkconfig, 'w') as f:
    json.dump(data, f, indent=4)

dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y%m%d-%H%M%S")
directory = 'reports-' + timestampStr
path = os.path.join(os.getcwd(), directory)
os.mkdir(path)

replicas = 5 # test replicas for each send rate
rounds = 3 # test rounds: open, query and transfer
for tps in SEND_RATES:
    with open('benchmarks/scenario/simple/config.yaml','r') as f:
        y=yaml.safe_load(f)
        for i in range(rounds):
            y['test']['rounds'][i]['rateControl']['opts']['tps'] = tps
    with open('benchmarks/scenario/simple/config.yaml','w') as f:
        yaml.dump(y,f,default_flow_style=False, sort_keys=False)

    for i in range(replicas):
        subprocess.run(['docker-compose', 'up'])
        subprocess.run(['cp', 'report.html', '{}/report-{}-{}.html'.format(directory, tps, i+1)])
        subprocess.run(['sleep', '10'])