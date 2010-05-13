import os
import os.path
import sys
import re

rootdir = "/var/www/testpilot/storage/4"

outfilename = "survey-answers.csv"

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

    return surveyAnswers


if __name__ == "__main__":
    outfile = open(outfilename, 'w')
    outfile.write("How long used firefox, multiple browsers, What browsers, Multi browser reason, skill level, gender, time on web, age, fx version, os, locale")

    used_firefox_answers = [0, 0, 0, 0, 0]
    multiple_browser_answers = [0, 0]
    what_browser_answers = [0, 0, 0, 0, 0]
    multi_browser_reason_answers = [0, 0, 0, 0, 0]
    skill_level_answers = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    gender_answers = [0, 0]
    time_on_web_answers = [0, 0, 0, 0, 0]
    age_answers = [0, 0, 0, 0, 0, 0]

    all_answers = [used_firefox_answers, multiple_browser_answers, what_browser_answers, multi_browser_reason_answers, skill_level_answers, gender_answers, time_on_web_answers, age_answers]

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
        locale = metadata[3]

        # Survey Answers here:
        surveyAnswers = getAllSurveyAnswers(lines)

        match = re.search( "^\[\[(.*)\]\]$", surveyAnswers)
        if match:
            surveyAnswers = match.group(1).split("],[")
            for i in [0, 1, 4, 5, 6, 7]:
                answer = surveyAnswers[i]
                answer = answer.strip("\"")
                if answer:
                    answer_number = int(answer)
                    if (answer_number == -1):
                        print "THIS IS A NEGATIVE ONE"
                    all_answers[i][answer_number] += 1

            for i in [2, 3]:
                answer = surveyAnswers[i]
                answerParts = answer.split(",")
                for part in answerParts:
                    match = re.search( "^\"(\d+)\"$", part)
                    if match:
                        answer_number = int(match.group(1))
                        all_answers[i][answer_number] += 1
                    elif len( part.strip("\"")) > 0:
                        all_answers[i][-1] += 1
        else:
            print "No response, skipping"
 

print all_answers
 
