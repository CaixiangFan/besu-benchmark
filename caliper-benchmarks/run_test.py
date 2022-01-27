import yaml, subprocess, os, json, sys
from datetime import datetime
import pandas as pd
import numpy as np

# WATCHDOG_ADDRESS = "192.168.226.176"
WATCHDOG_ADDRESS = "10.2.1.9"
# keyFile = "../data/rrg-bpet"
keyFile = "../data/bpet.pem"
current_directory = os.getcwd()
key = os.path.join(current_directory, keyFile)

subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", "get_results.py",
    "ubuntu@{}:/home/ubuntu/".format(WATCHDOG_ADDRESS)])

COMMAND = 'python3 get_results.py'
subprocess.Popen(["ssh", "-i", key, 
                    "-o", "StrictHostKeyChecking=no", "ubuntu@%s" % WATCHDOG_ADDRESS, COMMAND],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
subprocess.run(['sleep', '3'])
subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 
    "ubuntu@{}:/home/ubuntu/results.json".format(WATCHDOG_ADDRESS), current_directory])

subprocess.run(['sleep', '2'])

with open('results.json', 'r') as f:
    data = json.load(f)
    rows = data['results']

df_orig = pd.DataFrame(np.array(rows),
    columns=['Hostname', 'IP', 'NodeAddress', 'IsValidator'])

# sort dataframe
df = df_orig.copy()
idx = []
for name in df.Hostname:
    idx.append(int(name.split('-')[1]))
df['Index'] = idx
df = df.set_index(keys=df.Index).drop(labels='Index', axis=1).sort_index()

print(df)

DEFAULT_IP = df.IP.values[0]
SEND_RATES = [50, 100, 150, 200, 250]
# SEND_RATES = [40, 80, 120, 160, 200]
connection_url = "ws://" + DEFAULT_IP + ":8546"
if len(sys.argv) > 1:
    connection_url = "ws://" + sys.argv[1] + ":8546"
networkconfig = 'networks/4node-ibft2/networkconfig.json'
with open(networkconfig, 'r') as f:
    data = json.load(f)
    data['ethereum']['url'] = connection_url
with open(networkconfig, 'w') as f:
    json.dump(data, f, indent=4)

timestampStr = datetime.now().strftime("%Y%m%d-%H%M%S")
directory = 'reports/' + timestampStr
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

print(df)

subprocess.run(['sleep', '10'])

for _, row in df.iterrows():
    COMMAND = 'docker logs $(docker ps -q) > {}.log'.format(row['Hostname'])
    subprocess.Popen(["ssh", "-i", key, 
                        "-o", "StrictHostKeyChecking=no", "ubuntu@%s" % row['IP'], COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

subprocess.run(['sleep', '10'])

timestampStr = datetime.now().strftime("%Y%m%d-%H%M%S")
directory = '../data/logs-' + timestampStr
log_path = os.path.join(os.getcwd(), directory)
os.mkdir(log_path)
# collect besu logs
for _, row in df.iterrows():
    subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 
    "ubuntu@{}:/home/ubuntu/{}.log".format(row['IP'], row['Hostname']), log_path])
# collect caliper logs
subprocess.run(['mv', 'caliper.log', log_path])