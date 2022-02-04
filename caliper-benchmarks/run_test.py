import yaml, subprocess, os, json, sys
from datetime import datetime
import pandas as pd
import numpy as np
from dotenv import dotenv_values
import openstack
env = dotenv_values(".env")

def create_connection(auth_url, region, project_name, username, password,
                      user_domain, project_domain):
    return openstack.connect(
        auth_url=auth_url,
        project_name=project_name,
        username=username,
        password=password,
        region_name=region,
        user_domain_name=user_domain,
        project_domain_name=project_domain,
        app_name='bpet',
        app_version='1.0',
    )
    
def collect_info(WATCHDOG_ADDRESS, key):
    conn = create_connection(auth_url=env['OS_AUTH_URL'], region=env['OS_REGION_NAME'],
        project_name=env['OS_PROJECT_NAME'], username=env['OS_USERNAME'],
        password=env['OS_PASSWORD'], user_domain=env['OS_USER_DOMAIN_NAME'],
        project_domain=env['OS_PROJECT_DOMAIN_NAME'])
    
    subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", "get_nodeinfo.py",
    "ubuntu@{}:/home/ubuntu/".format(WATCHDOG_ADDRESS)])

    COMMAND = 'python3 get_nodeinfo.py'
    subprocess.Popen(["ssh", "-i", key, 
                        "-o", "StrictHostKeyChecking=no", "ubuntu@%s" % WATCHDOG_ADDRESS, COMMAND],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    subprocess.run(['sleep', '3'])
    subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 
        "ubuntu@{}:/home/ubuntu/nodeinfo.json".format(WATCHDOG_ADDRESS), os.getcwd()])

    subprocess.run(['sleep', '2'])

    with open('nodeinfo.json', 'r') as f:
        data = json.load(f)
        rows = data['nodeinfo']

    for row in rows:
        instance_id = conn.compute.find_server(row[0]).id
        host_id = conn.compute.get_server(instance_id).host_id
        row.append(instance_id)
        row.append(host_id)
    df = pd.DataFrame(np.array(rows),
        columns=['NodeName', 'IP', 'NodeAddress', 'IsValidator', 'InstanceID', 'HostID'])
    # sort dataframe
    df['Index'] = [int(name.split('-')[1]) for name in df.NodeName]
    df = df.set_index(keys=df.Index).drop(labels='Index', axis=1).sort_index()
    
    with open('nodeinfo.json', 'w') as f:
        json.dump({'nodeinfo': rows}, f, indent=4)
    return df

def run(WATCHDOG_ADDRESS, key, SEND_RATES):
    df = collect_info(WATCHDOG_ADDRESS, key)

    DEFAULT_IP = df.IP.values[0]
    connection_url = "ws://" + DEFAULT_IP + ":8546"
    # if len(sys.argv) > 1:
    #     connection_url = "ws://" + sys.argv[1] + ":8546"
    networkconfig = 'networks/ibft2/networkconfig.json'
    benchconfig = 'benchmarks/scenario/simple/config.yaml'

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
        with open(benchconfig,'r') as f:
            y=yaml.safe_load(f)
            for i in range(rounds):
                y['test']['rounds'][i]['rateControl']['opts']['tps'] = tps
        with open(benchconfig,'w') as f:
            yaml.dump(y,f,default_flow_style=False, sort_keys=False, indent=4)

        for i in range(replicas):
            subprocess.run(['docker-compose', 'up'])
            subprocess.run(['mv', 'report.html', '{}/report-{}-{}.html'.format(directory, tps, i+1)])
            subprocess.run(['sleep', '10'])

    print(df)

    subprocess.run(['sleep', '10'])

    for _, row in df.iterrows():
        COMMAND = 'docker logs $(docker ps -q) > {}.log'.format(row['NodeName'])
        subprocess.Popen(["ssh", "-i", key, 
                            "-o", "StrictHostKeyChecking=no", "ubuntu@%s" % row['IP'], COMMAND],
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    subprocess.run(['sleep', '10'])

    collect_log(df, key)

def collect_log(df, key):
    timestampStr = datetime.now().strftime("%Y%m%d-%H%M%S")
    directory = '../data/logs-' + timestampStr
    log_path = os.path.join(os.getcwd(), directory)
    os.mkdir(log_path)
    # collect besu logs
    for _, row in df.iterrows():
        subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 
        "ubuntu@{}:/home/ubuntu/{}.log".format(row['IP'], row.NodeName), log_path])
    # collect caliper logs
    subprocess.run(['mv', 'caliper.log', log_path])
    # collect node info json data
    subprocess.run(['mv', 'nodeinfo.json', log_path])
    

if __name__ == "__main__":
    # watchdogAddress = "192.168.226.176"
    watchdogAddress = "10.2.1.9"
    # keyFile = "../data/rrg-bpet"
    keyFile = "../data/bpet.pem"
    current_directory = os.getcwd()
    sshKey = os.path.join(current_directory, keyFile)
    sendRates = [50, 100, 150, 200, 250]
    run(watchdogAddress, sshKey, sendRates)