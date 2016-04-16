import sys
import csv

'''
This script is called after the copyscan finishes.
It adds the finished sdm file NAME and the target
Number, which is also called scan number into the 
complete.csv.
Ex:
$ python add_finish_to_complete.py 14A-425_1233.2341 10

or

$python add_finish_to_complete.py $sdmfile $scan
'''

def add_finish_to_complete(sdmfile, scan):
     '''This function adds the sdmfile name and its scan target number after it finishes copyscan'''
     with open("complete.csv", "a") as completeFile:
          completeWriter = csv.writer(completeFile, lineterminator = "\n")
          completeWriter.writerow([sdmfile] + [scan])
     return True

sdmfile = str(sys.argv[1]) #whatever machine you created
scan = str(sys.argv[2]) #listsdms.txt
add_finish_to_complete(sdmfile, scan)