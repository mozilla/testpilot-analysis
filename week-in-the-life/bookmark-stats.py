import os
import os.path
import sys
import re

rootdir = "/var/www/testpilot/storage/2"

outfilename = "bookmark-stats.csv"

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
    print "Survey Answers line is " + surveyAnswers
    if not "]" in surveyAnswers:
        return []
    return surveyAnswers.split("],[")


if __name__ == "__main__":
    outfile = open(outfilename, 'w')
    outfile.write("bookmarks, folders, depth, how_long_used_firefox, skill_level, time_on_web, age, sex\n")
    for file in os.listdir(rootdir):
        path = os.path.join( rootdir, file )
    
        print "Processing %s." % path

        f = open(path, 'r')
        lines = f.readlines()
        f.close()

        totalBookmarks = -1
        totalFolders = 0
        greatestDepth = 0

        # Start from the end, look backwards for the latest bookmark status event:
        linenum = len(lines) - 1
        while linenum > 0:
            line = lines[linenum]
            cells = line.split(",")
            try:
                eventCode = int( cells[0] )
            except ValueError:
                break
            if eventCode == 8:
                totalBookmarks = int( cells[1] )
                totalFolders = int( cells[2] )
                greatestDepth = int( cells[3] )
                break
            linenum -= 1

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

        if totalBookmarks > -1:
            print "Bookmarks: %d; Folders: %d; Depth: %d" % (totalBookmarks, totalFolders, greatestDepth)
            outfile.write( "%d, %d, %d, %d, %d, %d, %d, %d\n" % \
                               (totalBookmarks, totalFolders, greatestDepth, usedFirefox, skill, webTime, age, sex) )
    outfile.close()
