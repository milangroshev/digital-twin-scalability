#!/bin/bash
# Assemble docker image. 
echo 'Remember that you need to list and add your xauth keys into the Dockerfile for this to work.'

# ROS variables phisical robot
#ROS_MASTER_URI="http://169.254.200.200:11311"
#ROS_MASTER_URI="http://169.254.210.4:11311"
#ROS_IP="169.254.210.1"

# ROS variables simulated robot
ROS_MASTER_URI="http://10.0.1.2:11311"
ROS_IP="10.0.1.3"

INTERFACE_HOST="10.0.1.4"
SIM_HOST="10.0.1.2"


# Networking settings phisical robot
#sudo docker run \
#	--hostname niryo-one-control \
#	-it \
#	--rm \
#	--net=robot_eth_macvlan \
#        --ip=169.254.210.1 \
#	-e DISPLAY=$DISPLAY \
#        -e ROS_MASTER_URI=$ROS_MASTER_URI \
#        -e ROS_IP=$ROS_IP \
#	-e XAUTHORITY=$XAUTH \
#	-v $XSOCK:$XSOCK  \
#	-v $XAUTH:$XAUTH \
#	--add-host niryo-one-control:127.0.0.1 \
#	--add-host coppeliaSim:127.0.0.1 \
#        --add-host niryo-desktop:169.254.200.200 \
#        --add-host niryo-one-motion:169.254.210.2 \
#        --add-host niryo-one-interface:169.254.210.3 \
#        --add-host niryo-one-sim:169.254.210.4 \
#	niryo-one-control:latest \
#  	bash
#	--user root \

# Networking settings simulated robot
docker run \
       --hostname niryo-one-control \
       -it \
       --network test-net \
       --ip=$ROS_IP \
       -e ROS_MASTER_URI=$ROS_MASTER_URI \
       -e ROS_IP=$ROS_IP \
       --add-host niryo-one-control:127.0.0.1 \
       --add-host niryo-one-interface:$INTERFACE_HOST \
       --add-host niryo-one-sim:$SIM_HOST \
       niryo-one-control:latest \
#       bash
#        --user root \
