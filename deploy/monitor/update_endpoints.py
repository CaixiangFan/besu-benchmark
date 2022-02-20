import yaml
hostnames = []
host_ips = []

with open('./monitor/prometheus-template.yml') as f:
    prometheus = yaml.safe_load(f)
    endpoint = prometheus['scrape_configs'][1]
    for i in range(len(hostnames)):
        hostname = hostnames[i]
        host_ip = host_ips[i]
        prometheus['scrape_configs'][i+1] = endpoint
        prometheus['scrape_configs'][i+1]['job_name'] = 'push-gateway' + '-' + hostname
        prometheus['scrape_configs'][i+1]['static_configs'][0]['targets'][0] = host_ip + ':9091'

with open('./monitor/prometheus.yml', 'w') as f:
    yaml.dump(prometheus, f, indent=2)