import os
import os.path
import sys

eventNames = ["invalid", "open", "close", "drag", "drop", "switch", "load", "startup", "shutdown", "open window", "close window"]
eventFrequencies = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

rootdir = "/var/www/testpilot/storage/1-csv"

if __name__ == "__main__":
    for file in os.listdir(rootdir):
        path = os.path.join( rootdir, file )
    
        print "Processing %s." % path

        f = open(path, 'r')
        lines = f.readlines()
        f.close()

        linenum = 0
        for line in lines:
            linenum += 1
            if linenum == 1:
                continue # skip first line

            cells = line.split(",")
            eventCode = int( cells[0] )
            eventFrequencies[eventCode] += 1


    for i in range(len(eventNames) ):
        print "%s : %d" % (eventNames[i], eventFrequencies[i])
