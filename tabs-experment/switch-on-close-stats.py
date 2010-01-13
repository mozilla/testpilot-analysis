import os
import os.path
import sys

OPEN_EVENT = 1
CLOSE_EVENT = 2
DRAG_EVENT = 3
DROP_EVENT = 4
SWITCH_EVENT = 5
LOAD_EVENT = 6
OPEN_WINDOW_EVENT = 9
CLOSE_WINDOW_EVENT = 10

rootdir = "/var/www/testpilot/storage/1-csv"

outfile = "switch-on-close-stats.dat"

# Indices for BigHonkingArray:
SAME_SITE = 0
DIFFERENT_SITE = 1
EVERYTHING = 2

NUM_CLOSE_EVENTS = 0
ONE_SECOND = 1
TWO_SECONDS = 2
THREE_SECONDS = 3
FIVE_SECONDS = 4
TEN_SECONDS = 5
LATER = 6

# for tab group values:
UNKNOWN = -1

# TODO tab site hash info is only in load events!!!!!  That means to find what group the closed tab belongs to, we have to find the last
# load event before the tab was closed....!  Same for the last load event in the switched-to tab... Gross, we are now in the position of having to
# follow the whole history of each tab.

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


def processOneFile( filename, bigHonkingArray ):
    print "Processing %s." % filename

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    lastCloseEventTime = 0
    numSwitchEvents = 0
    closedTabGroup = UNKNOWN
    defaultIsSameSite = 0
    switchedToSameSite = 0
    totalCloseEvents = 0
    linenum = 0
    openWindows = {}

    for line in lines:
        linenum += 1
        if linenum == 1:
            continue # skip first line

        cells = line.split(",")
        eventCode = int( cells[0] )
        tabIndex = int(cells[1])
        windowIndex = int(cells[2])
        timestamp = long(cells[6] )

        if not openWindows.has_key(windowIndex):
            openWindows[windowIndex] = {}
        windowStore = openWindows[windowIndex]

        if eventCode == OPEN_EVENT:
            windowStore = adjustTabIndices(windowStore, tabIndex, 1)
            tabGroup = int(cells[4] )
            windowStore[tabIndex] = UNKNOWN
            openWindows[windowIndex] = windowStore

        if eventCode == LOAD_EVENT:
            # Store the tab group from the load event into openWindows for later use.
            tabGroup = int(cells[4] )
            windowStore[tabIndex] = tabGroup

        if eventCode == CLOSE_EVENT:
            bigHonkingArray[EVERYTHING][NUM_CLOSE_EVENTS] += 1
            numSwitchEvents = 0
            lastCloseEventTime = timestamp
            if windowStore.has_key(tabIndex):
                closedTabGroup = windowStore[tabIndex]
                del windowStore[tabIndex]
            else:
                closedTabGroup = UNKNOWN
            windowStore = adjustTabIndices(windowStore, tabIndex, -1)
            openWindows[windowIndex] = windowStore
        if eventCode == SWITCH_EVENT:
            numSwitchEvents += 1
            if windowStore.has_key(tabIndex):
                tabGroup = windowStore[tabIndex]
            else:
                tabGroup = UNKNOWN
            if numSwitchEvents == 1:
                # The first switch after the close event is the automatic switch.
                # Is it same site as the closed event?
                # print "Tab group on first switched event is %d, on the closed tab it was %d." % ( tabGroup, closedTabGroup)
                if tabGroup == UNKNOWN or closedTabGroup == UNKNOWN:
                    defaultIsSameSite = UNKNOWN
                elif tabGroup == closedTabGroup:
                    defaultIsSameSite = SAME_SITE
                    bigHonkingArray[SAME_SITE][NUM_CLOSE_EVENTS] += 1
                else:
                    defaultIsSameSite = DIFFERENT_SITE
                    bigHonkingArray[DIFFERENT_SITE][NUM_CLOSE_EVENTS] += 1
            if numSwitchEvents == 2:
                if tabGroup == closedTabGroup:
                    switchedToSameSite = True
                else:
                    switchedToSameSite = False
                delta = timestamp - lastCloseEventTime

                if delta <= 1000:
                    bigHonkingArray[EVERYTHING][ONE_SECOND] += 1
                elif delta <= 2000:
                    bigHonkingArray[EVERYTHING][TWO_SECONDS] += 1
                elif delta <= 3000:
                    bigHonkingArray[EVERYTHING][THREE_SECONDS] += 1
                elif delta <= 5000:
                    bigHonkingArray[EVERYTHING][FIVE_SECONDS] += 1
                elif delta <= 10000:
                    bigHonkingArray[EVERYTHING][TEN_SECONDS] += 1
                else:
                    bigHonkingArray[EVERYTHING][LATER] += 1

                if defaultIsSameSite != UNKNOWN:
                    if delta <= 1000:
                        bigHonkingArray[defaultIsSameSite][ONE_SECOND] += 1
                    elif delta <= 2000:
                        bigHonkingArray[defaultIsSameSite][TWO_SECONDS] += 1
                    elif delta <= 3000:
                        bigHonkingArray[defaultIsSameSite][THREE_SECONDS] += 1
                    elif delta <= 5000:
                        bigHonkingArray[defaultIsSameSite][FIVE_SECONDS] += 1
                    elif delta <= 10000:
                        bigHonkingArray[defaultIsSameSite][TEN_SECONDS] += 1
                    else:
                        bigHonkingArray[defaultIsSameSite][LATER] += 1

if __name__ == "__main__":
    bigHonkingArray = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]

    if len(sys.argv) == 1:
        for file in os.listdir(rootdir):
            path = os.path.join( rootdir, file )
            processOneFile( path, bigHonkingArray )
    elif len(sys.argv) == 2:
        processOneFile( sys.argv[1], bigHonkingArray )
        
print "Total close events: %d" % bigHonkingArray[EVERYTHING][NUM_CLOSE_EVENTS]

for i in [ONE_SECOND, TWO_SECONDS, THREE_SECONDS, FIVE_SECONDS, TEN_SECONDS, LATER]:
    print "Num switched in %d seconds: %d" % (i, bigHonkingArray[EVERYTHING][i] )

print

print "In %d of those, default tab was same site as closed tab." % bigHonkingArray[SAME_SITE][NUM_CLOSE_EVENTS]


for i in [ONE_SECOND, TWO_SECONDS, THREE_SECONDS, FIVE_SECONDS, TEN_SECONDS, LATER]:
    print "Num switched in %d seconds: %d" % (i, bigHonkingArray[SAME_SITE][i] )

print

print "In %d of those, default was not same site as closed tab." % bigHonkingArray[DIFFERENT_SITE][NUM_CLOSE_EVENTS]

for i in [ONE_SECOND, TWO_SECONDS, THREE_SECONDS, FIVE_SECONDS, TEN_SECONDS, LATER]:
    print "Num switched in %d seconds: %d" % (i, bigHonkingArray[DIFFERENT_SITE][i] )
