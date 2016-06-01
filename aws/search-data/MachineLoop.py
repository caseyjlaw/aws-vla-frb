import subprocess
import os.path

print("start process")
nameList = []
numOfMachine = 2
machineBaseName = 'machine'
for i in range(numOfMachine):
    machineName = machineBaseName + str(i)
    subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)
    nameList.append(machineName)

for name in nameList:
    print("name: ", name)
    subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
    subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)
