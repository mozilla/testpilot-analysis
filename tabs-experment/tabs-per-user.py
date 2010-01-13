import os.path
import os
import sys

OPEN_EVENT = 1
CLOSE_EVENT = 2
OPEN_WINDOW_EVENT = 9
CLOSE_WINDOW_EVENT = 10

OUTFILE = "tabs-per-user.dat"
ROOTDIR = "/var/www/testpilot/storage/1-csv"

HEADER = "min, avg, max\n"

# For each user, calculate maximum, minimum, and average (time-weighted average) tabs
# then generate histograms of max, min, avg on same axes.


outfile = open( OUTFILE, "w" )
outfile.write( HEADER )
for filename in os.listdir( ROOTDIR ):
    path = os.path.join( ROOTDIR, filename )
    print "Analyzing %s." % path
    infile = open( path, "r")
    lines = infile.readlines()
    infile.close()

    myMaxTabs = 0
    myMinTabs = 9999
    numTabsByWindow = {}
    tabsTimeSeries = []
    lineNum = 0
    for line in lines:
        lineNum += 1
        if lineNum == 1:
            continue
        cells = line.split(",")
        eventCode = int(cells[0])
        win = int(cells[2])
        numTabs = int(cells[5])
        timestamp = long(cells[6])
        if eventCode == OPEN_WINDOW_EVENT or eventCode == CLOSE_WINDOW_EVENT:
            numTabsByWindow[win] = 0
        if eventCode == OPEN_EVENT or eventCode == CLOSE_EVENT:
            numTabsByWindow[win] = numTabs
            totalTabs = sum(numTabsByWindow.values())
            tabsTimeSeries.append( ( timestamp, totalTabs ) )
            if totalTabs > myMaxTabs:
                myMaxTabs = totalTabs
            if totalTabs < myMinTabs:
                myMinTabs = totalTabs

    previousTime = 0
    total = 0
    if len( tabsTimeSeries) == 0:
        continue
    totalMs = tabsTimeSeries[-1][0] - tabsTimeSeries[0][0] 
    if totalMs == 0:
        continue

    for datapoint in tabsTimeSeries:
        # time-weighted average
        if (previousTime > 0):
            ms = datapoint[0] - previousTime
            numTabs = datapoint[1]
            total += numTabs * ms
        previousTime = datapoint[0]

    print "Duration of file is %d ms." % totalMs
    meanTabs = float(total) / float(totalMs)

    print "Min = %d, Avg = %f, Max = %d." % ( myMinTabs, meanTabs, myMaxTabs )

    outfile.write( "%d, %f, %d\n" % (myMinTabs, meanTabs, myMaxTabs ))

outfile.close()
        
