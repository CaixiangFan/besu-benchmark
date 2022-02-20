docker run --rm -d \
    --name grafana \
    -p 3000:3000 \
    grafana/grafana

sleep 5

docker run --rm -d \
    --name prometheus \
    -p 9090:9090 \
    -v ${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus