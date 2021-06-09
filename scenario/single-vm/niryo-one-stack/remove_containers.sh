#!/bin/bash
# Assemble docker image.

docker kill $(docker ps -a -q)

sleep 2

docker rm $(docker ps -a -q)

docker ps -a
