import sys

if __name__ == '__main__':
    machineName = str(sys.argv[1])
    f = open("machineNames.txt","r")
    lines = f.readlines()
    f.close()

    f = open("machineNames.txt","w")
    for line in lines:
    	if line != machineName+"\n":
    		f.write(line)
    f.close()
