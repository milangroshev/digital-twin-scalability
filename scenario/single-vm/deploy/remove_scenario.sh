#!/bin/bash


    ssh niryo@10.5.1.202 /home/niryo/digital-twin-scalability/scenario/digital-twin-vnf/remove_containers.sh

    sleep 2

    ssh niryo@10.5.1.201 /home/niryo/digital-twin-scalability/scenario/control-vnf/remove_containers.sh

    sleep 2
    
    ssh niryo@10.5.1.200 /home/niryo/digital-twin-scalability/scenario/robot-simulation-vnf/remove_containers.sh

    sleep 2

    /home/niryo/digital-twin-scalability/scenario/remote-controllers-vnf/remove_containers.sh

    sleep 2
    

