#!/bin/bash
# Assemble docker image. 
echo 'Remember that you need to list and add your xauth keys into the Dockerfile for this to work.'


XAUTH_KEYS_="$(xauth list $HOSTNAME/unix:0)"
sudo docker build . -t niryo-one-sim --build-arg "XAUTH_KEYS_=$XAUTH_KEYS_"

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
sudo docker run \
        --hostname niryo-one-sim \
        -it \
        --rm \
        --network test-net \
        --ip=10.0.1.1 \
        -e ROS_IP=10.0.1.1 \
        -e ROS_MASTER_URI=http://10.0.1.1:11311 \
        --add-host niryo-one-sim:127.0.0.1 \
        --add-host niryo-one-interface:10.0.1.3 \
        --add-host niryo-one-control:10.0.1.2 \
        niryo-one-sim:latest \
#       bash
#       --user root \
