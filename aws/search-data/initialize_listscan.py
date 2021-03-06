import subprocess
import sys
import csv
import os.path

'''
This script runs the listsdms and outputs all the sdm names to listsdms.txt.
Afterward, it does listscans to find the target and put it with its corresonding
sdmName in target.csv. Every time you run this script, a new header line will be
appended into the complete.csv to indicate the beginning of each copyscan
'''

#These variables must be set before running the script
#subprocess.call("export AWS_ACCESS_KEY_ID=$(aws configure get aws_access_key_id) AWS_SECRET_ACCESS_KEY=$(aws configure get aws_secret_access_key)", shell=True)
#subprocess.call("docker-machine create " + strname + " --driver virtualbox", shell=True)
#subprocess.call("eval $(docker-machine env " + strname + ")", shell=True)
#subprocess.call("export config="-m 7G -p 8888:8888 -v /home/ubuntu:/work -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY", shell=True)

def docker_rock(listsdms_txt = "listsdms.txt"):
     subprocess.call("docker run --rm -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY caseyjlaw/rtpipe-aws listsdms > " + listsdms_txt, shell=True)
     print('Updated sdm list at {0}'.format(listsdms_txt))

     with open(listsdms_txt, "r+") as outfile:
           sdmName_list = []
           '''Turning the content in the listsdms.txt in to a list of sdm file names. '''
           for line in outfile:
                 sdmName_list = line.replace("[", "").replace(" ", "").replace("]", "").replace("u", "").replace("'", "").split(",")
     print('Parsed sdm list from text into python')

     '''do the list scan for each single sdm file and append the result into target.csv'''
     with open("target.csv", "w") as targetFile:
          targetWriter = csv.writer(targetFile, lineterminator = "\n")
          targetWriter.writerow(["sdmName"] + ["scan number"] + ['type'] + ["size"])

     for sdmName in sdmName_list:
          if ("gains" not in sdmName):
               temp_txt = sdmName + ".txt"
               if not os.path.exists(temp_txt):
                    print('Writing scan list to {0}...'.format(temp_txt))
                    subprocess.call("docker run --rm -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY caseyjlaw/rtpipe-aws listscans " + sdmName + " > " + temp_txt, shell=True)
               else:
                    print('Reading scan list from {0}...'.format(temp_txt))

               filter_target(temp_txt, sdmName)

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

if (len(sys.argv) == 2):
  docker_rock(str(sys.argv[2]))
else:
  docker_rock()
