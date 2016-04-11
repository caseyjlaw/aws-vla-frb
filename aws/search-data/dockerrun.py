import subprocess
import sys
import csv


def docker_rock(dockerMachine_name, listsdms_txt):
     subprocess.call("export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)", shell=True)
     subprocess.call("docker-machine create " + dockerMachine_name + " --driver virtualbox", shell=True)
     subprocess.call("eval $(docker-machine env " + dockerMachine_name + ")", shell=True)
     subprocess.call("docker run --rm -v ~/.aws/:/.aws caseyjlaw/rtpipe-aws listsdms > listsdms.txt", shell=True)
     with open(listsdms_txt, "r+") as outfile:
           sdmName_list = []
           '''Turning the content in the listsdms.txt in to a list of sdm file names. '''
           for line in outfile:
                 sdmName_list = line.replace("[", "").replace("]", "").replace("u", "").replace("'", "").split(",")
                 
     '''do the list scan for each single sdm file and append the result into target.csv'''
     with open("target.csv", "w+") as targetFile:
          targetWriter = csv.writer(targetFile, lineterminator = "\n")
          targetWriter.writerow(["sdmName"] + ["scan number"] + ['type'] + ["size"])
     for sdmName in sdmName_list:
          if ("gains" not in sdmName):
               temp_txt = sdmName + ".txt"
               subprocess.call("docker run --rm $config caseyjlaw/rtpipe-aws listscans " + sdmName + " > " + temp_txt, shell=True)
               filter_target(temp_txt, sdmName)

     '''fill in the code: do the search in here. use next_to_search() to get the next sdmfile and
        scan to run copyscan. Add the sdmfile and scan to the complete.csv after finish running
        copyscan on them.'''
     with open("complete.csv", "w+") as completeFile:
          completeWriter = csv.writer(completeFile, lineterminator = "\n")
          completeWriter.writerow(["sdmName"] + ["scan number"])
    
     return True

def filter_target(tempOutput_txt, sdmName):
     '''This function does the target-filtering process for the temparory output txt file from listscan,
        and append the target to the target.csv
        return True after the process finishes. '''
     with open(tempOutput_txt, "r") as tempFile, open("target.csv", "a") as targetFile:
           targetWriter = csv.writer(targetFile, lineterminator = "\n")
           for line in tempFile:
                 if ("TARGET" in line):
                       line = line.split(",")
                       targetWriter.writerow([sdmName] + [line[0].split(":")[0].split(" ")[1]] + [line[1]] + [line[2]])
     return True

def add_finish_to_complete(sdmfile, scan):
     '''This function adds the sdmfile name and its scan target number after it finishes copyscan'''
     with open("complete.csv", "a") as completeFile:
          completeWriter = csv.writer(completeFile, lineterminator = "\n")
          completeWriter.writerow([sdmfile] + [scan])
     return True
          
def next_to_search():
     '''This function return the next sdmName and its scan target number that are not in the complete.csv,
        if there is not such sdmName and scan target number, return false.
        return type: (sdmName, scan target number) '''
     with open("complete.csv", "r") as completeFile, open("target.csv", "r") as targetFile:
          targetReader = csv.DictReader(targetFile)
          completeReader = csv.DictReader(completeFile)
          targetRow = [(row['sdmName'], row['scan number']) for row in targetReader]
          completeRow = [(row['sdmName'], row['scan number']) for row in completeReader]
          for rowtuple in targetRow:
               if rowtuple not in completeRow:
                    return rowtuple
     return False

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
     return True

dockerMachine_name = str(sys.argv[1]) #search
listsdms_txt = str(sys.argv[2]) #listsdms.txt
docker_rock(dockerMachine_name, listsdms_txt)

                                  
                
