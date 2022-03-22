#!bin/bash
docker exec -it $(docker ps --format '{{.Names}}' | grep besu) java $BESU_OPTS -XX:+PrintFlagsFinal -version | grep -Ei "maxheapsize|maxram"