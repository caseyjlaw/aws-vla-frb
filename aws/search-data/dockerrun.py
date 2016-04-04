import subprocess
import sys
import csv

dockerMachine_name = str(sys.argv[1]) #search
listsdms_txt = str(sys.argv[2]) #listsdms.txt
#only run one of the tests below at a time
readin(dockerMachine_name, listsdms_txt)
#test_single_file_scan()
#test_filter_target()


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

def test_single_file_scan():
     '''the below section is JUST for testing the listscan command with the sample listsdms.txt we have at this point'''
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
                           targetWriter.writerow(["scan number"] + ['type'] + ["size"])
                           for line in tempFile:
                                if ("TARGET" in line):
                                     line = line.split(",")
                                     targetWriter.writerow([line[0]] + [line[1]] + [line[2]])


def test_filter_target():
     '''The below section is Just for testing target-filtering process for the doc.txt, the sample output file
        from the listscan'''
     with open("doc.txt", "r") as tempFile, open("target.csv", "w+") as targetFile:
           targetWriter = csv.writer(targetFile, lineterminator = "\n")
           targetWriter.writerow(["scan number"] + ['type'] + ["size"])
           for line in tempFile:
                 if ("TARGET" in line):
                       line = line.split(",")
                       targetWriter.writerow([line[0]] + [line[1]] + [line[2]])                               
                                  
                
