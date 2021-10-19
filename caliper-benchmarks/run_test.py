import yaml, subprocess

tps_list = [40, 80, 120, 160, 200]
for tps in tps_list:
    with open('benchmarks/scenario/simple/config.yaml','r') as f:
        y=yaml.safe_load(f)
        for i in range(3):
            y['test']['rounds'][i]['rateControl']['opts']['tps'] = tps
    with open('benchmarks/scenario/simple/config.yaml','w') as f:
        yaml.dump(y,f,default_flow_style=False, sort_keys=False)

    for i in range(5):
        subprocess.run(['docker-compose', 'up'])
        subprocess.run(['cp', 'report.html', 'reports/report-{}-{}.html'.format(tps, i+1)])
        subprocess.run(['sleep', '10'])