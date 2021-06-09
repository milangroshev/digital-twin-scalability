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
        --add-host niryo-one-sim:$SIM_HOST \
        --add-host niryo-stack:127.0.0.1 \
	--privileged=true \
        -v /home/user/logs:/home/niryo/scripts/logs \
        niryo-one-full-stack
#       bash
#       --user root \
