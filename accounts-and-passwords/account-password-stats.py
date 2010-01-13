import os
import os.path
import sys
import re

rootdir = "/var/www/testpilot/storage/3"

outfilename = "account-password-stats-all.csv"

def parseSurveyAnswer(substring):
    match = re.search( "\d+", substring)
    if match:
        return int( match.group(0))
    else:
        return -1

def freeformSurveyAnswer(substring):
    parts = substring.split(",")
    parts = [x for x in parts if x != "\"\""]
    if len(parts) == 0:
        return "-1"
    if len(parts) == 1:
        return parts[0].strip("\"")
    else:
        return ";".join([x.strip("\"") for x in parts])

def getAccountSurveyAnswers(inputText):
    if not "]" in inputText:
        return []
    return inputText.split("],[")

if __name__ == "__main__":
    outfile = open(outfilename, 'w')
    outfile.write("happiness, open_id, other_tools, multi_accounts_same_website, share_computer, fx_version, os, locale, num_extensions, total_sites, total_passwords, most_used, histogram\n")
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

        totalSites = 0
        totalPasswords = 0
        mostUsed = 0
        passwordFrequencies = []
        surveyAnswers = ""

        headerIsOver = False
        dataIsOver = False
        for line in lines:
            # skip headers:
            if not headerIsOver:
                # In the header
                if "password_id, frequency" in line:
                    headerIsOver = True
                continue

            elif not dataIsOver:
                # In the data
                if "password_survey_answers" in line:
                    dataIsOver = True
                    continue
                cells = line.split(",")
                try:
                    frequency = int( cells[1] )
                    totalSites += frequency
                    totalPasswords += 1
                    if frequency > mostUsed:
                        mostUsed = frequency
                    passwordFrequencies.append( str(frequency) )
                    
                except ValueError:
                    print "Error parsing event code or timestamp.  Skipping this file."
                    break

            else:
                # Survey answers  
                surveyAnswers = surveyAnswers + line

        answers = getAccountSurveyAnswers(surveyAnswers)
        if len(answers) == 0:
            happiness = -1
            openID = -1
            otherTools = -1
            multiAccountsSameWebsite = -1
            shareComputer = -1
        else:
            # question 0: do you share your computer?
            # question 1: Do you use multiple accounts for the same website?
            # question 6: Do you use other tools to manage your password?
            # question 7: openID?
            # question 8: How do you feel?
            try:
                happiness = parseSurveyAnswer( answers[8] )
                openID = freeformSurveyAnswer( answers[7] )
                otherTools = freeformSurveyAnswer( answers[6] )
                multiAccountsSameWebsite = parseSurveyAnswer( answers[1] )
                shareComputer = parseSurveyAnswer( answers[0] )
            except:
                print "Error parsing survey answers!"
                continue
        
        histogram = ";".join( passwordFrequencies )

        # "happiness, open_id, other_tools, multi_accounts_same_website, share_computer, fx_version, os, locale, num_extensions, total_sites, total_passwords, most_used, histogram\n"
        outfile.write( "%d, %s, %s, %d, %d, %s, %s, %s, %d, %d, %d, %d, %s\n" % \
                           (happiness, openID, otherTools, multiAccountsSameWebsite, shareComputer, fxVersion, OS, locale, numExtensions, totalSites, totalPasswords, mostUsed, histogram))
    outfile.close()
