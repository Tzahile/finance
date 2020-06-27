#!/usr/bin/env bash

CONTAINER_NAME="fin-redis"

docker stop ${CONTAINER_NAME} &> /dev/null
docker rm   ${CONTAINER_NAME} &> /dev/null

docker run --name ${CONTAINER_NAME} -p 6379:6379 -v redis.conf:/redis.conf -d redis redis-server /redis.conf
