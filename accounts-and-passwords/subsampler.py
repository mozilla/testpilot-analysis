import os
import random

inFileName = "account-password-stats-all.csv"

infile = open(inFileName, "r")

allLines = infile.readlines()
header = allLines[0]
dataLines = allLines[1:]

infile.close()

numDataLines = len(dataLines)
print "There are %d lines in the source file." % numDataLines

def makeSubSample(dataLines, header, percent, outFileName):
    print "Generating %d\ percent sample." % percent
    print "Shuffling..."
    random.shuffle(dataLines)

    n = int( numDataLines * percent / 100)
    print "Selecting %d percent, or %d." % (percent, n)

    subSample = dataLines[:n]

    outfile = open(outFileName, "w")
    outfile.write(header)
    for line in subSample:
        outfile.write(line)
    outfile.close()


makeSubSample(dataLines, header, 10, "account-password-stats-10.csv")
makeSubSample(dataLines, header, 30, "account-password--stats-30.csv")
makeSubSample(dataLines, header, 50, "account-password-stats-50.csv")
makeSubSample(dataLines, header, 70, "account-password-stats-70.csv")
