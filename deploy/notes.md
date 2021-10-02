# WATCHDOG_ADDRESS
192.168.23.64

# Redis
## Deployment
```
docker run -d -v /opt/besu/redis-data:/data --name besu-redis --restart=always -p 6379:6379 redis:6.2.5

docker run --rm -it -e REDIS_1_HOST=127.0.0.1 -e REDIS_1_NAME=besu-redis -p 18001:80 erikdubbelboer/phpredisadmin
```

## Schema
* DB0 - miscellaneous
* DB1 - hosts
  * ip:hostname
* DB2 - enode
  * enode:url
  * master:ip
* DB3 - deployment logs
  * ip:logs