docker run --rm -d \
    --name pushgateway \
    -p 9091:9091 \
    prom/pushgateway

sleep 5

docker run --rm -d \
    --name prometheus \
    -p 9090:9090 \
    -v /home/ubuntu/bpet/deploy/monitor/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus