#!/bin/bash
# Assemble docker image. 

ROS_MASTER_URI="http://10.0.1.2:11311"
ROS_IP="10.0.1.2"

INTERFACE_HOST="10.0.1.4"
CONTROL_HOST="10.0.1.3"


# 5TONIC Networking settings
#sudo docker run \
#	--hostname niryo-one-sim \
#	-it \
#	--rm \
#	--net=robot_eth_macvlan \
#       --ip=169.254.210.4 \
#        -e ROS_IP=169.254.210.4 \
#        -e ROS_MASTER_URI=http://169.254.210.4:11311 \
#	-e DISPLAY=$DISPLAY \
#	-e XAUTHORITY=$XAUTH \
#	-v $XSOCK:$XSOCK  \
#	-v $XAUTH:$XAUTH \
#	--add-host niryo-one-sim:127.0.0.1 \
#	--add-host dtwin:127.0.0.1 \
#       --add-host niryo-desktop:169.254.200.200 \
#        --add-host niryo-one-motion:169.254.210.2 \
#        --add-host niryo-one-interface:169.254.210.3 \
#        --add-host niryo-one-control:169.254.210.1 \
#	niryo-one-sim:latest \
#  	bash
#	--user root \

# 5TONIC Networking settings
docker run \
        --hostname niryo-one-sim \
        -it \
        --hostname niryo-one-sim \
        --network test-net \
        --ip=$ROS_IP \
        -e ROS_IP=$ROS_IP \
        -e ROS_MASTER_URI=$ROS_MASTER_URI \
        --add-host niryo-one-sim:127.0.0.1 \
        --add-host niryo-one-interface:$INTERFACE_HOST \
        --add-host niryo-one-control:$CONTROL_HOST \
        niryo-one-sim:latest 
