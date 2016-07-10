import sys
import csv
import subprocess

numOfMachine = int(sys.argv[1])

if (len(sys.argv) == 3):
    machineBaseName = str(sys.argv[2])
else:
    machineBaseName = 'test'
  
with open("machineList.csv", "w+") as machineList:
    machineWriter = csv.writer(machineList, lineterminator = "\n")
    for i in range(numOfMachine):
        machineName = machineBaseName + str(i)
        subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.2xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)
        machineWriter.writerow([machineName])
        
