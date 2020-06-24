#!/usr/bin/env bash

CONTAINER_NAME="mongo"

if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
fi

docker run -d --name $CONTAINER_NAME -p 27017:27017 mongo