#!/bin/bash
# Assemble docker image. 
echo 'Remember that you need to list and add your xauth keys into the Dockerfile for this to work.'

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

# Lab Networking settings
ROS_MASTER_URI="http://10.0.1.$1:11311"
ROS_IP="10.0.1.$(($1 + 2))"

CONTROL_HOST="10.0.1.$(($1 + 1))"
SIM_HOST="10.0.1.$1"

# Lab Networking settings
docker run \
        --hostname niryo-one-interface \
        -dit \
        --rm \
        --net=test-net \
        --ip=$ROS_IP \
        -e ROS_MASTER_URI=$ROS_MASTER_URI \
        -e ROS_IP=$ROS_IP \
        --add-host niryo-one-control:$CONTROL_HOST \
        --add-host niryo-one-sim:$SIM_HOST \
        --add-host niryo-one-interface:127.0.0.1 \
        niryo-one-interface:latest \
#       bash
#       --user root \
