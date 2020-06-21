#!/usr/bin/env bash

docker stop fin-redis &> /dev/null
docker rm fin-redis   &> /dev/null

docker run -d --name fin-redis -p 6379:6379  -v redis.conf:/redis.conf redis redis-server /redis.conf
