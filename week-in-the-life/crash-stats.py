import os
import os.path
import sys
import re

rootdir = "/var/www/testpilot/storage/2"

outfilename = "crash-stats.csv"
maxCrashes = 0
maxCrashFile = ""

# We go through each line and keep track of the browser state with a state machine.
if __name__ == "__main__":
    outfile = open(outfilename, 'w')
    outfile.write("crashes, num_sessions, avg_session_length, total_session_length, fx_version, os, num_extensions\n")
    for file in os.listdir(rootdir):
        path = os.path.join( rootdir, file )
    
        print "Processing %s." % path

        f = open(path, 'r')
        lines = f.readlines()
        f.close()

        metadata = lines[1].split(",")
        fxVersion = metadata[0]
        OS = metadata[4].strip("\n")
        numExtensions = len( lines[3].split(",") )

        numSessions = 0
        totalSessionTime = 0
        lastSessionStartTime = 0

        numCrashes = 0
        headerIsOver = False
        browserNotShutdown = False
        for line in lines:
            if not headerIsOver:
                if "event_code" in line:
                    headerIsOver = True
                continue
            cells = line.split(",")
            eventCode = int( cells[0] )
            timestamp = int( cells[4] )
            if lastSessionStartTime == 0:
                lastSessionStartTime = timestamp

            # TODO: eliminate duplicate startup events
            if eventCode == 1:
                # We actually expect an 8 (bookmark-status) and a 14 (addon-status) before the start event!!!
                # In that order.
                # browser start
                lastSessionStartTime = timestamp
                if browserNotShutdown:
                    numCrashes += 1
                    numSessions += 1
                    sessionTime = timestamp - lastSessionStartTime # TODO bad assumption here
                    totalSessionTime += sessionTime
                    browserNotShutdown = False
            elif eventCode == 8 or eventCode == 14:
                # These normally come right before the startup code, and should be ignored.
                pass
            elif eventCode == 2 or eventCode == 3:
                # Shutdown or restart
                sessionTime = timestamp - lastSessionStartTime
                totalSessionTime += sessionTime
                numSessions += 1
                browserNotShutdown = False
            else:
                # Any other event -browser running fine; consider it to have been started up!
                browserNotShutdown = True

        if numSessions > 0:
            avgSessionTime = totalSessionTime / numSessions
        else:
            avgSessionTime = 0
        outfile.write("%d, %d, %f, %d, %s, %s, %d\n" % (numCrashes, numSessions, avgSessionTime, totalSessionTime, fxVersion, OS, numExtensions) )

        if numCrashes > maxCrashes:
            maxCrashFile = file
            maxCrashes = numCrashes

print "Maximum crashes was %d in file %s." % ( maxCrashes, maxCrashFile )
outfile.close()
