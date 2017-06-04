#!/bin/bash

eval $(docker-machine env $machineName)
export config="-m $memory -p 8888:8888 -v /home/ubuntu:/work -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"

count=`docker ps -a |grep Up | wc -l`
if (($count < 1)); then
#    git pull   # only needed for distributed submission
    sdmfile=`python next_to_search_sdm.py`
    scan=`python next_to_search_scan.py`
    if ((${#sdmfile} > 0)); then
#    git commit -am 'starting a job'   # only needed for distributed submission
#    git push 
	echo Running search on $sdmfile $scan
	docker run -d $config caseyjlaw/rtpipe-aws search $sdmfile $scan --paramfile rtpipe_c42xlarge.conf
        OUT=$?
        if [ $OUT -eq 0 ];then
            echo Adding $sdmfile $scan to finished list
            python add_finished_to_complete.py $sdmfile $scan
        else
            echo Submission error. Not adding $sdmfile $scan to finished list
        fi
    else
	echo 'No sdm to search'
    fi
else
    if ((cleanup == true)); then
	echo Process Up, skipping this machine.
    else
	echo removing $machineName
	docker-machine rm -f $machineName
	python removeMachine.py $machineName $region
	aws ec2 delete-key-pair --key-name $machineName
    fi
fi

