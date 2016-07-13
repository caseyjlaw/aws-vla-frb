error=`docker-machine ls | grep $machineName | grep Error | wc -l`
if (($error > 0)); then
	docker-machine rm -f $machineName
	python removeMachine.py $machineName
