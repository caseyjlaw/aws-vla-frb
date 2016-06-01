import sys
import csv
import subprocess

numOfMachine = int(sys.argv[1])
print(numOfMachine)
machineBaseName = 'machine'
with open("machineList.csv", "w+") as machineList:
    machineWriter = csv.writer(machineList, lineterminator = "\n")
    for i in range(numOfMachine):
        machineName = machineBaseName + str(i)
        subprocess.call("docker-machine create " + machineName + " --driver virtualbox", shell=True)
        machineWriter.writerow([machineName])
        
