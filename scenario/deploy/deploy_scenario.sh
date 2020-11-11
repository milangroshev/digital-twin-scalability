#!/bin/bash

instances=$1

step=$(($instances * 3))

for i in `seq 2 3 $step`; do 
    
    echo $i;
    ssh niryo@10.5.1.200 /home/niryo/digital-twin-scalability/scenario/robot-simulation-vnf/deploy_containers.sh $i

    sleep 20

    ssh niryo@10.5.1.201 /home/niryo/digital-twin-scalability/scenario/control-vnf/deploy_containers.sh $i

    sleep 20

    ssh niryo@10.5.1.202 /home/niryo/digital-twin-scalability/scenario/digital-twin-vnf/deploy_containers.sh $i

    sleep 20

    if (( $i == 2)) ; then
      /home/niryo/digital-twin-scalability/scenario/remote-controllers-vnf/deploy_container.sh $i
    fi

    sleep 600

done

