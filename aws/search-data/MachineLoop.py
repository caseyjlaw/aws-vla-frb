import subprocess
import os.path
import sys
import time

print("start process")
assert (len(sys.argv) == 2), "Missing the machine base name. Format: python MachineLoop.py <machineBaseName>"
nameList = []
numOfMachine = 3
machineBaseName = str(sys.argv[1])
for i in range(numOfMachine):
    machineName = machineBaseName + str(i)
    subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)
    nameList.append(machineName)

while (True):
    for name in nameList:
        print("name: ", name)
        subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
        subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)
    time.sleep(30)
    
