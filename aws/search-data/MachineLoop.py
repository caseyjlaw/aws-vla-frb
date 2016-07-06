import subprocess
import os.path
import sys
import time

'''
python MachineLoop.py <machineBaseName> <numOfMachine> [<spotPrice>]
'''

def createMachine(machineName, spotPriceMode, spotPrice = 0):
    if spotPriceMode:
        subprocess.call("docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-request-spot-instance --amazonec2-spot-price " + spotPrice + " " + machineName, shell=True)
    else:
        subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)

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
    f = open("machineNames.txt", "w")
    for i in range(numOfMachine):
        machineName = machineBaseName + str(i)
        if spotPriceMode:
            subprocess.call("docker-machine create --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-request-spot-instance --amazonec2-spot-price " + spotPrice + " " + machineName, shell=True)
        else:
            subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region us-west-2 --amazonec2-instance-type c4.xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY", shell=True)
        f.write(machineName + "\n")
        time.sleep(3)
    f.close()

    '''Begin doing the scan-search'''
    while (True):
        f = open("machineNames.txt", "r")
        nameList = f.readlines()
        f.close()

        if len(nameList) < numOfMachine:
            f = open("machineNames.txt", "a")
            i += 1
            createMachine(machineBaseName + str(i), spotPriceMode, spotPrice)
            f.write(machineBaseName + str(i))
            f.close()

        for name in nameList:
            name = name[:-1]
            print("name: ", name)
            #subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
            #subprocess.call("machineName="+name+" ./SearchScanLoop.sh", shell=True)
        time.sleep(30)

    
