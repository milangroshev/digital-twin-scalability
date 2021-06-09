#!/bin/bash

instances=$1

step=$(($instances * 2))

for i in `seq 2 2 $step`; do 
    
    echo $i;
    ssh user@10.5.1.167 /home/user/digital-twin-scalability/scenario/single-vm/robot-simulation-vnf/deploy_containers.sh $i

    sleep 20

    ssh user@10.5.1.156 /home/user/digital-twin-scalability/scenario/single-vm/niryo-one-stack/deploy_containers.sh $i

    sleep 20
    #sleep 600

done

