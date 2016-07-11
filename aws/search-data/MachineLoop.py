import subprocess
import os.path
import sys
import time

'''
python MachineLoop.py <machineBaseName> <numOfMachine> [<spotPrice>]
'''

def createMachine(machineName, spotPriceMode, spotPrice = 0):
    if spotPriceMode:
        subprocess.call("docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.2xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-request-spot-instance --amazonec2-spot-price " + spotPrice + " " + machineName, shell=True)
    else:
        subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.2xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)

'''Main function'''
if __name__ == '__main__':
    '''Getting necessary information from passed in arguments'''
    print("start process")
    assert (len(sys.argv) >= 3), "Missing the machine base name. Format: python MachineLoop.py <machineBaseName> <numOFMachine>"
    machineBaseName = str(sys.argv[1])
    numOfMachine = int(sys.argv[2])
    spotPriceMode = False
    spotPrice = 0

    if (len(sys.argv) == 4):
        spotPrice = str(sys.argv[3])
        spotPriceMode = True

    '''Machine creation'''
#    f = open("machineNames.txt", "w")
#    for i in range(numOfMachine):
#        machineName = machineBaseName + str(i)
#        createMachine(machineName, spotPriceMode, spotPrice)
#        f.write(machineName + "\n")
#        time.sleep(3)
#    f.close()

    '''Begin doing the scan-search'''
    subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
    i = 0
    while (True):
        with open("machineNames.txt", "r") as f:
            nameList = f.readlines()

        if len(nameList) < numOfMachine:
            i += 1
            name = machineBaseName + str(i)
            createMachine(name, spotPriceMode, spotPrice)
            subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)

            with open("machineNames.txt", "a") as f:
                f.write(name + "\n")

        time.sleep(30)

    
