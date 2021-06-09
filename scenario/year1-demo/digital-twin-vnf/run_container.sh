#!/bin/bash
# Assemble docker image. 
echo 'Remember that you need to list and add your xauth keys into the Dockerfile for this to work.'

# 5TONIC Networking settings
#ROS_MASTER_URI="http://169.254.210.4:11311"
#ROS_IP="169.254.210.3"

# Lab Networking settings
ROS_MASTER_URI="http://10.0.1.2:11311"
ROS_IP="10.0.1.4"

CONTROL_HOST="10.0.1.3"
SIM_HOST="10.0.1.2"

# Lab Networking settings
docker run \
        --hostname niryo-one-interface \
        -it \
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
