import json, subprocess, os
key = "../data/rrg-bpet"
watchdogAddress = "192.168.226.176"

subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 
        "ubuntu@{}:/home/ubuntu/nodeinfo.json".format(watchdogAddress), os.getcwd()])

with open('nodeinfo.json') as f:
    rows = json.load(f)['nodeinfo']

for row in rows:
    subprocess.run(['scp', '-i', key, "-o", "StrictHostKeyChecking=no", 'restart.sh',
        "ubuntu@{}:/home/ubuntu/bpet/deploy".format(row[1])])
    COMMAND = 'sh restart.sh'
    subprocess.Popen(["ssh", "-i", key, 
                    "-o", "StrictHostKeyChecking=no", "ubuntu@{}:/home/ubuntu".format(row[1]), COMMAND],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)