import sys

if __name__ == '__main__':
    machineName = str(sys.argv[1])
    region = str(sys.argv[2])
    with open("machineNames_{0}.txt".format(region),"r") as f:
        lines = f.readlines()

    with open("machineNames_{0}.txt".format(region),"w") as f:
        for line in lines:
            if machineName not in line:
                f.write(line)
