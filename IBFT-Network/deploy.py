import re, subprocess, os, sys, json, toml, socket, time

if len(sys.argv) < 2:
    print('Default values will be used. NODE_COUNT is 4\n')
    NODE_COUNT = 4  # number of concu
else:
    print('Default values have been overwritten.')
    NODE_COUNT = int(sys.argv[1])

# Step 1: create directories
curr_dir = os.getcwd()

for i in range(NODE_COUNT):
    path = os.path.join(curr_dir, 'Node-{}'.format(i+1))
    if not os.path.isdir(path):
        os.mkdir(path)
    data_path = os.path.join(os.getcwd(), 'Node-{}/data'.format(i+1))
    if not os.path.isdir(data_path):
        os.mkdir(data_path)

# Step 2: create a configuration file
with open('ibftConfigFile-template.json', 'r') as f:
    ibft_config = json.load(f)
    ibft_config['blockchain']['nodes']['count'] = NODE_COUNT
with open('ibftConfigFile.json', 'w') as f:
    json.dump(ibft_config, f, indent=4)

# Step 3: Generate node keys and a genesis file
credential_dir = os.path.join(curr_dir, 'networkFiles')
if not os.path.isdir(credential_dir):
    subprocess.run(['sh', 'create_artifacts.sh'])
    time.sleep(20 + NODE_COUNT * 0.2)

# Ste 4. Copy the genesis file to the IBFT-Network directory
subprocess.run(['cp', 'networkFiles/genesis.json', './'])

# Step 5. Copy the node private keys to the node directories
dir_list = os.listdir('networkFiles/keys')
for i in range(NODE_COUNT):
    subprocess.run(['cp', 'networkFiles/keys/{}/key'.format(dir_list[i]), 'Node-{}/data/'.format(i+1)])
    subprocess.run(['cp', 'networkFiles/keys/{}/key.pub'.format(dir_list[i]), 'Node-{}/data/'.format(i+1)])
    subprocess.run(['cp', 'start.sh', 'Node-{}/'.format(i+1)])

# Step 6. Set up toml config
DEFAULT_P2P_PORT = 30303
DEFAULT_RPC_HTTP_PORT = 8545
DEFAULT_RPC_WS_PORT = 8445

with open('Node-1/data/key.pub', 'r') as f:
    key = f.read()
    enode_id = key[2:]
enode_host = '127.0.0.1'
enode_port = '30303'
enode_url = ['enode://{}@{}:{}'.format(enode_id, enode_host, enode_port)]
for i in range(NODE_COUNT):
    with open('config-template.toml', 'r') as f:
        config = toml.load(f)
    config['identity'] = 'Node-{}'.format(i+1)
    config['p2p-port'] = DEFAULT_P2P_PORT + i
    config['rpc-http-port'] = DEFAULT_RPC_HTTP_PORT + i
    config['rpc-ws-port'] = DEFAULT_RPC_WS_PORT + i
    if i > 0:
        config['bootnodes'] = enode_url
    # config['p2p-host'] = host_ip
    # config['rpc-http-host'] = host_ip
    # config['rpc-ws-host'] = host_ip
    # config['metrics-push-host'] = host_ip
    with open('Node-{}/config.toml'.format(i+1), 'w') as f:
        toml.dump(config, f)

# Step 7. deploy the network
base_dir = curr_dir
for i in range(NODE_COUNT):
    home_path = os.path.join(base_dir, 'Node-{}'.format(i+1))
    os.chdir(home_path)
    subprocess.run(['sh', 'start.sh', 'Node-{}'.format(i+1), 
        str(DEFAULT_P2P_PORT + i), str(DEFAULT_RPC_HTTP_PORT + i), str(DEFAULT_RPC_WS_PORT + i)])