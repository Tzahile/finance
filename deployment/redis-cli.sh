#!/usr/bin/env bash

CONTAINER_NAME="fin-redis"

docker exec -it ${CONTAINER_NAME} redis-cli
