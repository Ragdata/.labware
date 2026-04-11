#!/usr/bin/env bash

docker run -d \
  -p 29001:9001 \
  --name portainer_agent \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ${DOCKER_DIR:-'/var/lib/docker/volumes'}:/var/lib/docker/volumes \
  -v /:/host \
  portainer/agent:latest
