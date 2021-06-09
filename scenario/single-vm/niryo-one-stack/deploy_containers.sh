#!/bin/bash
# Assemble docker image. 

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

# Lab Networking settings
ROS_MASTER_URI="http://10.0.1.$1:11311"
ROS_IP="10.0.1.$(($1 + 1))"

SIM_DRIVERS="10.0.1.$1"

# Lab Networking settings
docker run \
        --hostname niryo-stack \
        -dit \
        --rm \
	--name stack-$1 \
        --net=test-net \
        --ip=$ROS_IP \
        -e ROS_MASTER_URI=$ROS_MASTER_URI \
        -e ROS_IP=$ROS_IP \
        --add-host niryo-one-sim:$SIM_DRIVERS \
        --add-host niryo-stack:$ROS_IP \
	--privileged=true \
        -v /home/user/logs:/home/niryo/scripts/logs \
        niryo-one-full-stack:latest
#       bash
#       --user root \
