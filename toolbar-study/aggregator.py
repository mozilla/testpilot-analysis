import os
import sys
import hashlib
import random

HEADER = "user, os, fx_version, event, item_id, interaction_type, timestamp\n"


FILENAME = "Toolbar-study-aggregated.csv"
outfile = open(FILENAME, "w")

outfile.write( HEADER )

rootdir = "/var/testpilot/storage/6"

user_num = 0
filenames = os.listdir(rootdir)

for filename in filenames:
    # Skip all the header stuff
    # Pull out the extensions, compare to list of known-bad extensions.
    filename = os.path.join( rootdir, filename.strip("\n") )

    infile = open( filename, "r")
    lines = infile.readlines()
    infile.close()

    try:
        metadata = lines[1].split(",")
        fxVersion = metadata[0]
        OS = metadata[4].strip("\n")
        extensions = lines[3].split(",")
    except:
        print "Can't parse this file."
        print lines
        continue
    numExtensions = len( extensions )
    locale = metadata[3]

    headerIsOver = False
    for line in lines:
        # skip headers:
        if not headerIsOver:
            # In the header
            if "event, item_id, interaction_type" in line:
                headerIsOver = True
            continue

        outfile.write( "%d, %s, %s, %s\n" % ( user_num, OS, fxVersion, line.strip("\n") ) )

    user_num += 1

outfile.close()
