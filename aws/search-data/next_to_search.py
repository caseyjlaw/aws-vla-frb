import csv

'''
This script looks for the name of the sdm file and the 
scan number of its target to be search next. It returns
two things sdmfile, scan
It is called after the listscan finishes and we have a 
target.csv to start with.
'''

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
                    print(rowtuple[0], rowtuple[1])
     return False

next_to_search()
