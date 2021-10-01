docker run --rm -d \
    --name pushgateway \
    -p 9091:9091 \
    prom/pushgateway

sleep 10

docker run --rm -d \
    --name prometheus \
    -p 9090:9090 \
    -v /home/ubuntu/IBFT-Network/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus

sleep 5

docker run --rm -d \
    --name grafana \
    -p 3000:3000 \
    grafana/grafana