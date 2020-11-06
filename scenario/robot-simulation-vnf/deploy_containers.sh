#!/bin/bash
# Assemble docker image. 


if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi


ROS_MASTER_URI="http://10.0.1.$1:11311"


ROS_IP="10.0.1.$1"


INTERFACE_HOST="10.0.1.$(($1 + 2))"

CONTROL_HOST="10.0.1.$(($1 + 1))"


# 5TONIC Networking settings
docker run \
        --hostname niryo-one-sim \
        -dit \
        --hostname niryo-one-sim \
        --network test-net \
        --ip=$ROS_IP \
        -e ROS_IP=$ROS_IP \
        -e ROS_MASTER_URI=$ROS_MASTER_URI \
        --add-host niryo-one-sim:127.0.0.1 \
        --add-host niryo-one-interface:$INTERFACE_HOST \
        --add-host niryo-one-control:$CONTROL_HOST \
        niryo-one-sim:latest 
