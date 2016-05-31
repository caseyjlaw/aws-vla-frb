import subprocess
import os.path

print("start process")
nameList = []
numOfMachine = 1
machineBaseName = 'machine'
for i in range(numOfMachine):
    machineName = machineBaseName + str(i)
    subprocess.call("docker-machine create " + machineName + " --driver virtualbox", shell=True)
    nameList.append(machineName)

for name in nameList:
    print("name: ", name)
    subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
    subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)
