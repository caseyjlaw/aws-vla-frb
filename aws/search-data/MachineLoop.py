import subprocess
import os.path
import sys
import time
'''
python MachineLoop.py <machineBaseName> <numOfMachine> [<spotPrice>]
'''
print("start process")
assert (len(sys.argv) >= 3), "Missing the machine base name. Format: python MachineLoop.py <machineBaseName> <numOFMachine>"
nameList = []
machineBaseName = str(sys.argv[1])
numOfMachine = int(sys.argv[2])
spotPriceMode = False

if (len(sys.argv) == 4):
    spotPrice = str(sys.argv[3])
    spotPriceMode = True

for i in range(numOfMachine):
    machineName = machineBaseName + str(i)
    if spotPriceMode:
        subprocess.call("docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-request-spot-instance --amazonec2-spot-price " + spotPrice + " " + machineName, shell=True)
    else:
        subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)
    nameList.append(machineName)
    time.sleep(3)

while (True):
    for name in nameList:
        print("name: ", name)
        subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
        subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)
    time.sleep(30)

    
