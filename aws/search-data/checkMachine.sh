#!/bin/bash

machineext=`docker-machine ls | grep $machineName$ | wc -l`
error=`docker-machine ls | grep $machineName$ | grep Error | wc -l`
if (($machineext == 1)); then
    if (($error > 0)); then
	docker-machine rm -f $machineName
	python removeMachine.py $machineName $region
    else
	machineName=$machineName memory=$memory ./SearchScanLoop.sh
    fi
else
    python removeMachine.py $machineName $region
    aws ec2 delete-key-pair --key-name $machineName
fi
