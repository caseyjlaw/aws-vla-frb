import subprocess
import os.path
import sys
import time

'''
python MachineLoop.py <machineBaseName> <numOfMachine> [<spotPrice>] [<region>] [<export memory>]
'''

def createMachine(machineName, spotPriceMode, region, spotPrice, zone='b'):
    if spotPriceMode:
        subprocess.call("docker-machine create --driver amazonec2 --amazonec2-region " + region + " --amazonec2-instance-type c4.2xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-zone " + zone + " --amazonec2-request-spot-instance --amazonec2-spot-price " + spotPrice + " " + machineName, shell=True)
    else:
        subprocess.call("docker-machine create " + machineName + " --driver amazonec2 --amazonec2-region " + region + " --amazonec2-instance-type c4.2xlarge --amazonec2-root-size 256 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-zone " + zone, shell=True)

'''Main function'''
if __name__ == '__main__':
    '''Getting necessary information from passed in arguments'''
    print("start process")
    assert (len(sys.argv) >= 3), "Missing the machine base name. Format: python MachineLoop.py <machineBaseName> <numOFMachine>"
    machineBaseName = str(sys.argv[1])
    numOfMachine = int(sys.argv[2])
    spotPriceMode = False
    spotPrice = 0
    region = "us-west-2"
    memory = "14G"
    zone = 'a'

    if (len(sys.argv) >= 4):
        spotPrice = str(sys.argv[3])
        spotPriceMode = True
    if (len(sys.argv) >= 5):
        region = str(sys.argv[4])
    if (len(sys.argv) >= 6):
        memory = str(sys.argv[5])
    if (len(sys.argv) >= 7):
        zone = str(sys.argv[6])

    '''Machine creation'''
    if not os.path.exists("machineNames_{0}.txt".format(region)):
        with open("machineNames_{0}.txt".format(region), "w") as f:
            f.write('')

#    for i in range(numOfMachine):
#        machineName = machineBaseName + str(i)
#        createMachine(machineName, spotPriceMode, region, spotPrice)
#        f.write(machineName + "\n")
#        time.sleep(3)
#    f.close()

    '''Begin doing the scan-search'''
    subprocess.call("chmod +x SearchScanLoop.sh", shell=True)
    subprocess.call("chmod +x checkMachine.sh", shell=True)
    while (True):
        with open("machineNames_{0}.txt".format(region), "r") as f:
            nameList = f.readlines()
            nameList = [name.rstrip('\n') for name in nameList]

        if len(nameList) < numOfMachine:
            print('{0} machines found. less than {1} so creating new machine.'.format(len(nameList), numOfMachine))
            i = max([int(name.split('-')[-1]) for name in nameList])+1
            machineName = '{0}-{1}-{2}'.format(machineBaseName, region, i)
            createMachine(machineName, spotPriceMode, region, spotPrice, zone=zone)
            time.sleep(30)
            subprocess.call('docker-machine ls > docker-machine_{0}.txt'.format(region), shell=True)
            subprocess.call("machineName="+machineName+" memory="+memory+ " region=" + region + " ./checkMachine.sh", shell=True)
#            subprocess.call("machineName="+machineName+" memory="+memory+" ./SearchScanLoop.sh", shell=True)

            with open("machineNames_{0}.txt".format(region), "a") as f:
                f.write(machineName + "\n")
        else:
            print('At numOfMachine limit of {0}. checking on their status.'.format(numOfMachine))
            subprocess.call('docker-machine ls > docker-machine_{0}.txt'.format(region), shell=True)
            for machineName in nameList:
                subprocess.call("machineName="+machineName+" memory="+memory+ " region=" + region + " ./checkMachine.sh", shell=True)

        time.sleep(60)

    
