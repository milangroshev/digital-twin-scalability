#!/bin/bash

instances=$1

step=$(($instances * 3))


for i in `seq 2 3 $step`; do 
    
    echo $i;
    ssh niryo@10.5.1.200 /home/niryo/digital-twin-scalability/scenario/robot-simulation-vnf/deploy_containers.sh $i

    sleep 2

    ssh niryo@10.5.1.201 /home/niryo/digital-twin-scalability/scenario/control-vnf/deploy_containers.sh $i

    sleep 2

    ssh niryo@10.5.1.202 /home/niryo/digital-twin-scalability/scenario/digital-twin-vnf/deploy_containers.sh $i

    sleep 2

done
