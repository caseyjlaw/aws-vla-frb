#!/bin/bash

numOfUp=0
function SearchScanLoop() {
	echo into the search
	eval $(docker-machine env $1)

	count=`docker ps -a |grep Up | wc -l`
	if (($count < 1)); then
	    git pull
	    sdmfile=`python next_to_search_sdm.py`
	    scan=`python next_to_search_scan.py`
	    python add_finished_to_complete.py $sdmfile $scan
	    git commit -am 'starting a job'
	    git push
	    contid=`docker run -d $config caseyjlaw/rtpipe-aws search $sdmfile $scan --paramfile rtpipe_c42xlarge.conf`
	else
		echo machine is in use
	fi
}
python createMachine.py $numOfMachine $machineBaseName

for i in $(more machineList.csv); do
	echo machine name $i
	SearchScanLoop $i
done
if (($numOfUp < 1)); then
    numOfMachine=$(($numOfMachine+1))
    python addMachine.py $numOfMachine $machineBaseName
else
	echo
fi
numOfUp=0
sleep 10

    
    
