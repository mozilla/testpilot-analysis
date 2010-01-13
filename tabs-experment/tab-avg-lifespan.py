import os.path
import sys

OPEN_EVENT = 1
CLOSE_EVENT = 2
DRAG_EVENT = 3
DROP_EVENT = 4
OPEN_WINDOW_EVENT = 9
CLOSE_WINDOW_EVENT = 10
OUTFILE = "lifespans-errorful.dat"

def adjustTabIndices(windowStore, minTabIndex, delta):
    # all entries in windowStore with index >= minTabIndex get their index changed by delta.
    # return adjusted version of windowStore.
    newWindowStore = {}
    for tabId in windowStore.keys():
        if tabId >= minTabIndex:
            newWindowStore[ tabId + delta ] = windowStore[tabId]
        else:
            newWindowStore[tabId] = windowStore[tabId]
    return newWindowStore


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: python tab-avg-lifespan.py infile.csv"
        sys.exit(1)

    inpath = sys.argv[1]

    print "Processing %s." % inpath

    f = open(inpath, 'r')
    lines = f.readlines()
    f.close()

    outfile = open(OUTFILE, "a")

    openWindows = {}
    tabLifespans = []
    linenum = 0
    numOpenAtBeginning = 0
    numOpenAtEnd = 0
    numOpenEvents = 0
    numCloseEvents = 0
    firstTimestamp = 0
    numDragEvents = 0
    numDropEvents = 0
    
    for line in lines:
        linenum += 1
        if linenum == 1:
            continue # skip first line

        cells = line.split(",")
        eventCode = int( cells[0] )
        tabIndex = int(cells[1] )
        windowIndex = int( cells[2] )
        timestamp = long(cells[6])

        if (firstTimestamp == 0):
            firstTimestamp = timestamp

        #if eventCode == OPEN_WINDOW_EVENT:
        #    openWindows[windowIndex] = {}
        #if eventCode == CLOSE_WINDOW_EVENT:
        #    del openWindows[windowIndex]

        #if not openWindows.has_key(windowIndex):
            # we have not seen this window before.  It is a window already open when we start tracking.  If it has tabs in it, then assign
            # those tabs an open date equal to the first timestamp in the file, to treat them as though they were opened at the start of the study.
            # openWindows[windowIndex] = {}
            #numTabsInWindow = int(cells[5])
            #for x in range(numTabsInWindow):
                # tabs are indexed starting from 1
                #openWindows[windowIndex][x+1] = firstTimestamp

        if not openWindows.has_key(windowIndex):
            openWindows[windowIndex] = {}

        windowStore = openWindows[windowIndex]

        if eventCode == OPEN_EVENT:
            numOpenEvents += 1
            #print "Opened tab %d in window %d at %d." % (tabIndex, windowIndex, timestamp)
            windowStore = adjustTabIndices(windowStore, tabIndex, 1)
            windowStore[tabIndex] = timestamp
            openWindows[windowIndex] = windowStore


        if eventCode == CLOSE_EVENT:
            numCloseEvents += 1
            if windowStore.has_key(tabIndex):
                lifespan = timestamp - windowStore[tabIndex]
                if (lifespan < 0 ):
                    raise "Negative lifespan: timestamp is %d and time at tab open was %d." % (timestamp, windowStore[tabIndex])
                tabLifespans.append(lifespan)
                del windowStore[tabIndex]
                windowStore = adjustTabIndices(windowStore, tabIndex, -1)
                # TODO Actually, tab indices should be adjusted whether or not we saw the open event for this tab!!!
                openWindows[windowIndex] = windowStore
            else:
                #print "I didn't see the open event for this tab."
                numOpenAtBeginning += 1
                lifespan = timestamp - firstTimestamp
                if (lifespan < 0 ):
                    raise "Negative lifespan: timestamp is %d and time at tab open was %d." % (timestamp, firstTimestamp)
                tabLifespans.append(lifespan)
                # This should never happen.
                # print "This is the second thing that shouldn't happen."

        if eventCode == DRAG_EVENT:
            #print "Drag Event!! TabIndex = %d, windowIndex = %d." % (tabIndex, windowIndex)
            numDragEvents += 1
        if eventCode == DROP_EVENT:
            #print "Drop Event!! TabIndex = %d, windowIndex = %d." % (tabIndex, windowIndex)
            numDropEvents +=1

    print "Finishing file..."
    # We're done: but let's close out any tabs stil open:
    lastTimestamp = timestamp
    for win in openWindows.keys():
        for tabIndex in openWindows[win]:
            #print "There's a tab still open: %d in window %d." % (tabIndex, win)
            lifespan = lastTimestamp - openWindows[win][tabIndex]
            if (lifespan < 0 ):
                raise "Negative lifespan: timestamp is %d and time at tab open was %d." % (lastTimestamp, openWindows[win][tabIndex])
            tabLifespans.append(lifespan)
            numOpenAtEnd += 1

    if numOpenAtEnd - numOpenAtBeginning != numOpenEvents - numCloseEvents:
        print "Checksum: openAtEnd - openAtBeginning = openEvents - closeEvents?  %d - %d = %d - %d ? %d = %d" % (numOpenAtEnd, numOpenAtBeginning, numOpenEvents,numCloseEvents, numOpenAtEnd - numOpenAtBeginning, numOpenEvents - numCloseEvents)
        raise "Checksum failed!"
    # print "Num drag events was %d, num drop events was %d." % (numDragEvents, numDropEvents)    
    print "Num lifespans found was %d." % len( tabLifespans )
    if len(tabLifespans) == 0:
        raise "No tab lifespans found in this file."

    # print "Lifespans: "
    # print tabLifespans

    totalLiff = 0
    for liff in tabLifespans:
        outfile.write( "%d\n" % liff )
        totalLiff += liff
    print "Average is %d." % ( totalLiff / len( tabLifespans ) )
    
    outfile.close()
