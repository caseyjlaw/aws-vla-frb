import subprocess
import sys
import csv

def readin(dockerMachine_name, listsdms_txt):
     subprocess.call("export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)", shell=True)
     subprocess.call("docker-machine create " + strname + " --driver virtualbox", shell=True)
     subprocess.call("eval $(docker-machine env " + strname + ")", shell=True)
     subprocess.call("docker run --rm -v ~/.aws/:/.aws caseyjlaw/rtpipe-aws listsdms > listsdms.txt", shell=True)
     with open(filename, "r+") as outfile:
           sdmName_list = []
           '''Turning the content in the listsdms.txt in to a list of sdm file names. '''
           for line in outfile:
                 sdmName_list = line.replace("[", "").replace("]", "").replace("u", "").replace("'", "").split(",")
           '''do the list scan for each single sdm file and put the result into <sdmName>-target.csv'''
           for sdmName in sdmName_list:
                 if ("gains" not in sdmName):
                       temp_txt = sdmName + ".txt"
                       target_csv = sdmName + "-target.csv"
                       subprocess.call("docker run --rm $config caseyjlaw/rtpipe-aws listscans " + sdmName + " > " + temp_txt, shell=True)
                       with open(temp_txt, "r") as tempFile, open(target_csv, "w+") as targetFile:
                             targetWriter = csv.writer(targetFile, lineterminator = "\n")
                             targetWriter.writerow(["scan number"] + ['type'] + ["size"])
                             '''filter out the line with "target" in it and write it to the target file. '''
                             for line in tempFile:
                                   if ("TARGET" in line):
                                        line = line.split(",")
                                        targetWriter.writerow([line[0]] + [line[1]] + [line[2]]) 



'''dockerMachine_name = str(sys.argv[1]) #search
listsdms_txt = str(sys.argv[2]) #listsdms.txt
readin(dockerMachine_name, listsdms_txt)'''

'''the below section is JUST for testing the listscan command, we already have the sample listsdms.txt at this point
   Comment out the following part if you decide to run the readin(...) function. '''

filename = str(sys.argv[1])
with open(filename, "r+") as outfile:
    sdmName_list = []
    
    #Turning the content in the listsdms.txt in to a list of sdm file names. 
    for line in outfile:
        sdmName_list = line.replace("[", "").replace("]", "").replace("u", "").replace("'", "").split(",")
        
    #do the list scan for each single sdm file and put the result into <sdmName>-target.csv
    for sdmName in sdmName_list:
          if ("gains" not in sdmName):
                temp_txt = sdmName + ".txt"
                target_csv = sdmName + "-target.csv"
                subprocess.call("docker run --rm $config caseyjlaw/rtpipe-aws listscans " + sdmName + " > " + temp_txt, shell=True)
                with open(temp_txt, "r") as tempFile, open(target_csv, "w+") as targetFile:
                      targetWriter = csv.writer(targetFile, lineterminator = "\n")
                      for line in tempFile:
                            if ("TARGET" in line):
                                  targetWriter.writerow([line])


'''The below section is Just for testing filtering process for the temp_txt output file
   comment out this part to run readin(...) function.'''
with open("doc.txt", "r") as tempFile, open("target.csv", "w+") as targetFile:
      targetWriter = csv.writer(targetFile, lineterminator = "\n")
      targetWriter.writerow(["scan number"] + ['type'] + ["size"])
      for line in tempFile:
            if ("TARGET" in line):
                  line = line.split(",")
                  targetWriter.writerow([line[0]] + [line[1]] + [line[2]])                               
                                  
                
