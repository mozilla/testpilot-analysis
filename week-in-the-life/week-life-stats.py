import os
import os.path
import sys
import re

rootdir = "/var/www/testpilot/storage/2"

outfilename = "week-life-stats-all.csv"

def parseSurveyAnswer(substring):
    match = re.search( "\d+", substring)
    if match:
        return int( match.group(0))
    else:
        return -1

def getAllSurveyAnswers(lines):
    # Survey answers should be on the 6th line, between
    # a line that says "survey_answers" and a line that says "experiment_data".
    # It can itself be multiple lines, if user entered any newlines in a freeform
    # text entry field.
    linenum = 5
    line = lines[linenum]
    surveyAnswers = ""
    while not "experiment_data" in line:
        surveyAnswers += line
        linenum += 1
        if linenum >= len( lines ):
            break   # can't happen?
        line = lines[linenum]
    if not "]" in surveyAnswers:
        return []
    return surveyAnswers.split("],[")


if __name__ == "__main__":
    outfile = open(outfilename, 'w')
    outfile.write("how_long_used_firefox, skill_level, time_on_web, age, sex, fx_version, os, locale, num_extensions, num_downloads, bookmarks, folders, depth, num_sessions, avg_session_length, total_session_length\n")
    for file in os.listdir(rootdir):
        path = os.path.join( rootdir, file )
    
        print "Processing %s." % path

        f = open(path, 'r')
        lines = f.readlines()
        f.close()

        totalBookmarks = 0
        totalFolders = 0
        greatestDepth = 0
        numDownloads = 0
        numSessions = 0
        totalSessionTime = 0
        lastSessionStartTime = 0
        metadata = lines[1].split(",")
        fxVersion = metadata[0]
        OS = metadata[4].strip("\n")
        numExtensions = len( lines[3].split(",") )
        locale = metadata[3]

        # Survey Answers here:
        surveyAnswers = getAllSurveyAnswers(lines)
        if len(surveyAnswers) == 0:
            usedFirefox = -1
            skill = -1
            sex = -1
            webTime = -1
            age = -1
        else:
            # question 0: how long have you used Firefox?
            # question 4: Skill level
            # question 5: sex
            # question 6: time on web
            # question 7: age
            try:
                usedFirefox = parseSurveyAnswer( surveyAnswers[0] )
                skill = parseSurveyAnswer( surveyAnswers[4] )
                sex = parseSurveyAnswer( surveyAnswers[5] )
                webTime = parseSurveyAnswer( surveyAnswers[6] )
                age = parseSurveyAnswer( surveyAnswers[7] )
            except:
                print "Error parsing survey answers!"
                continue
        

        numCrashes = 0
        headerIsOver = False
        browserNotShutdown = False
        # Go through, find bookmark status, downloads, sessions
        inHeader = True
        headerIsOver = False
        browserNotShutdown = False
        for line in lines:
            # skip headers:
            if not headerIsOver:
                if "event_code" in line:
                    headerIsOver = True
                continue
            cells = line.split(",")
            try:
                eventCode = int( cells[0] )
                timestamp = int( cells[4] )
            except ValueError:
                print "Error parsing event code or timestamp.  Skipping this file."
                break

            if lastSessionStartTime == 0:
                lastSessionStartTime = timestamp

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
                browserNotShutdown = True
            elif eventCode == 8:
                # Bookmark status!
                totalBookmarks = int( cells[1] )
                totalFolders = int( cells[2] )
                greatestDepth = int( cells[3] )
            elif eventCode == 14:
                # These normally come right before the startup code, and should be ignored.
                pass
            elif eventCode == 2 or eventCode == 3:
                # Shutdown or restart
                sessionTime = timestamp - lastSessionStartTime
                totalSessionTime += sessionTime
                numSessions += 1
                browserNotShutdown = False
            elif eventCode == 12:
                # Downloads
                numDownloads += 1
                browserNotShutdown = True
            else:
                # Any other event -browser running fine
                browserNotShutdown = True

        if numSessions > 0:
            avgSessionTime = totalSessionTime / numSessions
        else:
            avgSessionTime = 0

        print "Bookmarks: %d; Folders: %d; Depth: %d" % (totalBookmarks, totalFolders, greatestDepth)
        #"how_long_used_firefox, skill_level, time_on_web, age, sex, fx_version, os, locale, num_extensions, num_downloads, bookmarks, folders, depth, num_sessions, avg_session_length, total_session_length\n"
        outfile.write( "%d, %d, %d, %d, %d, %s, %s, %s, %d, %d, %d, %d, %d, %d, %d, %d\n" % \
                           (usedFirefox, skill, webTime, age, sex, fxVersion, OS, locale, numExtensions, numDownloads, totalBookmarks, totalFolders, greatestDepth, numSessions, avgSessionTime, totalSessionTime))
    outfile.close()
