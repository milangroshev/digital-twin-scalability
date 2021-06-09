#!/bin/bash

# Localhost Networking settings
ROS_MASTER_URI="http://10.0.1.$1:11311"
ROS_IP="10.0.1.$(($1 + 120))"

SIM_HOST="10.0.1.$1"
CONTROL_HOST="10.0.1.$(($1 + 1))"
INTER_HOST="10.0.1.$(($1 + 2))"

# Networking settings simulated robot

docker run \
  --hostname niryo-one-dtwin \
  -it \
  --rm \
  --net=test-net \
  --ip=$ROS_IP \
  -e ROS_MASTER_URI=$ROS_MASTER_URI \
  -e ROS_IP=$ROS_IP \
  --add-host niryo-one-dtwin:$ROS_IP \
  --add-host niryo-one-control:$CONTROL_HOST \
  --add-host niryo-one-interface:$INTER_HOST \
  --add-host niryo-one-sim:$SIM_HOST \
  --privileged=true \
  -v /home/niryo/logs:/home/niryo/logs \
  dtwin-web:latest \
#  bash
