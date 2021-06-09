#!/bin/bash
# Assemble docker image. 


if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi


ROS_MASTER_URI="http://10.0.1.$1:11311"
ROS_IP="10.0.1.$1"


STACK_HOST="10.0.1.$(($1 + 1))"

# 5TONIC Networking settings
docker run \
        --hostname niryo-one-sim \
        -dit \
	--name drivers-$1 \
        --network test-net \
        --ip=$ROS_IP \
        -e ROS_IP=$ROS_IP \
        -e ROS_MASTER_URI=$ROS_MASTER_URI \
        --add-host niryo-one-sim:127.0.0.1 \
        --add-host niryo-stack:$STACK_HOST \
        niryo-one-sim:latest 
