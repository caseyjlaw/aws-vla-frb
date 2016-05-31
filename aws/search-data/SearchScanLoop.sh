#!/bin/bash

echo into the search
eval $(docker-machine env $machineName)
export config="-m 7G -p 8888:8888 -v /home/ubuntu:/work -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY"

count=`docker ps -a |grep Up | wc -l`
if (($count < 1)); then
    git pull
    sdmfile=`python next_to_search_sdm.py`
    scan=`python next_to_search_scan.py`
    python add_finished_to_complete.py $sdmfile $scan
    git commit -am 'starting a job'
    git push
    contid=`docker run -d $config caseyjlaw/rtpipe-aws search $sdmfile $scan`
else
	echo machine is in use
fi
 
echo