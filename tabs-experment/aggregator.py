import os
import sys
import random

HEADER = "user, event_code, tab_position, tab_window, ui_method, tab_site_hash, num_tabs, timestamp\n"

if len( sys.argv ) != 4:
    print "Usage: python aggregator.py infile outfile sample-percentage"
    sys.exit(1)

print "Reading filenames from %s." % sys.argv[1]
directoryFile = open( sys.argv[1], "r")

filenames = directoryFile.readlines()
directoryFile.close()

print "Shuffling filenames..."
random.shuffle(filenames)

percentage = int( sys.argv[3] )
n_total = len( filenames )
n = int( n_total * percentage / 100 )

print "Will choose %d percent of %d files, or %d." % (percentage, n_total, n)
filenames = filenames[:n]

print "Will write to %s." % sys.argv[2]
outfile = open( sys.argv[2], "w")
outfile.write( HEADER )

user_num = 0
for filename in filenames:
    filename = filename.strip("\n")
    print "Processing %s." % filename
    infile = open( filename, "r")
    lines = infile.readlines()
    for i in range(1, len(lines)): # skip first because it's a header
        line = lines[i]
        cells = line.split(",")
        # take user number plus first six cells..
        outfile.write( "%d, %s, %s, %s, %s, %s, %s, %s\n" % (user_num, cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], cells[6]) )

    user_num += 1

outfile.close()
