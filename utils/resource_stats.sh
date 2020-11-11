#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: <net interface> <stat file location>"
    exit 1
fi

net_interface=$1

file=$2




echo 'timestamp,cpu,ram,tx_bytes,rx_bytes'>$file".csv"
seq=0
echo "Taking stats in " $file".csv"
end=$(($SECONDS+30))


while [ $SECONDS -lt $end ];
do

    #echo "Taking statistics"
    cpu=0.0
    ram=0.0
    seq=$(($seq+1))

    while read -r i
    do
        if [[ "$i" != *"CPU"* ]]; then
            #echo "line:" $i
            proc_cpu=`echo $i | awk '{print $1}'`
            #echo "proc_cpu: " $proc_cpu
            cpu=`echo $cpu + $proc_cpu | bc`
            #echo "cpu: " $cpu
            proc_ram=`echo $i | awk '{print $2}'`
            ram=`echo $ram + $proc_ram | bc`
            #name=`echo $i | awk '{print substr($0, index($0,$3))}'`
        fi
    done < <(ps aux | awk '{print $3,$4}')

    timestamp=$(date +%s%N)
    #echo $timestamp
    #echo "tottal CPU out: " $cpu
    #echo "tottal RAM: " $ram
    tx_bytes=`cat /sys/class/net/$net_interface/statistics/tx_bytes`
    rx_bytes=`cat /sys/class/net/$net_interface/statistics/rx_bytes`
    echo $timestamp,$cpu,$ram,$tx_bytes,$rx_bytes >> $file".csv"
    sleep 0.5
done

