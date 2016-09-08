#!/bin/bash

machineext=`cat docker-machine_$region.txt | awk '{ print $1 }' | grep $machineName$ | wc -l`
error=`cat docker-machine_$region.txt | awk '{ print $1$4 }' | egrep "${machineName}Unknown|${machineName}Error" | wc -l`
echo Status of $machineName in $region: $machineext $error
if (($machineext == 1)); then
    if (($error > 0)); then
	echo removing $machineName
	docker-machine rm -f $machineName
	python removeMachine.py $machineName $region
	aws ec2 delete-key-pair --key-name $machineName
    else
	echo beginning SearchScanLoop for $machineName
	machineName=$machineName memory=$memory ./SearchScanLoop.sh
    fi
else
    echo no machine found for $machineName. Removing locally.
    python removeMachine.py $machineName $region
    aws ec2 delete-key-pair --key-name $machineName
fi
