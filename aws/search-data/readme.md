#Steps To Run The Script
###### Do the following inside the aws-vla-frb/aws/search-data folder
```C
git pull

export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)

python MachineLoop.py <machineBaseName> <numOfMachine> [<spotPrice>]
```

#After Exiting The Script
###### MachineLoop.py runs an infinite loop, you can ctrl-c to stop it any time. All searches are running in the background. Stopping the python script does not stop the searching procedure. Following is the example of checking current running process:

```C
Juns-MBP:search-data juntan$ docker-machine ls
NAME   ACTIVE   DRIVER      STATE     URL                         SWARM   DOCKER    ERRORS
jun0   -        amazonec2   Running   tcp://54.187.250.188:2376           v1.11.2   
jun1   -        amazonec2   Running   tcp://54.186.160.96:2376            v1.11.2   
jun2   -        amazonec2   Running   tcp://54.201.144.248:2376           v1.11.2   
Juns-MBP:search-data juntan$ eval $(docker-machine env jun0)
Juns-MBP:search-data juntan$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
1af9885acafe        caseyjlaw/rtpipe-aws   "/entrypoint.sh searc"   16 minutes ago      Up 16 minutes   0.0.0.0:8888->8888/tcp   compassionate_liskov
Juns-MBP:search-data juntan$ eval $(docker-machine env jun1)
Juns-MBP:search-data juntan$ docker ps -a
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
c1745a56dbc0        caseyjlaw/rtpipe-aws   "/entrypoint.sh searc"   17 minutes ago      Up 17 minutes       0.0.0.0:8888->8888/tcp   admiring_bardeen
```
###### If the STATUS is Exited, you can do the following

```C
Juns-MBP:search-data juntan$ docker-machine rm jun0
```
###### check the bucket
```C
aws s3 ls s3://aka-vla-frb-cands2/...
```

# Flow Of The Script
###### MachineLoop.py calls SearchScanLoop.sh
###### SearchScanLoop.sh calls removeMachine.py, python next_to_search_sdm.py, python next_to_search_scan.py and add_finished_to_complete.py

