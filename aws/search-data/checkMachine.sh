#!/bin/bash

machineext=`docker-machine ls | awk '{ print $1 }' | grep $machineName$ | wc -l`
error=`docker-machine ls | awk '{ print $1 }' | grep $machineName$ | grep Error | wc -l`
echo Status of $machineName: $machineext $error
if (($machineext == 1)); then
    if (($error > 0)); then
	echo removing $machineName
	docker-machine rm -f $machineName
	python removeMachine.py $machineName $region
    else
	echo beginning SearchScanLoop for $machineName
	machineName=$machineName memory=$memory ./SearchScanLoop.sh
    fi
else
    echo no machine found for $machineName. Removing locally.
    python removeMachine.py $machineName $region
    aws ec2 delete-key-pair --key-name $machineName
fi
