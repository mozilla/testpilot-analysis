import simplejson
import sys
import os.path

def pyDictToCsv( pyObj, csvFile ):
    # header

    csvFile.write("event_code, tab_position, tab_window, ui_method, " + \
          "tab_site_hash, num_tabs, timestamp, extensions, location, version, os\n")
    contents = pyObj["contents"]
    extensions = pyObj["extensions"]
    rowNum = 0
    for row in contents:
        csvFile.write( "%d, " % row["event_code"] )
        csvFile.write( "%d, " % row["tab_position"] )
        csvFile.write( "%d, " % row["tab_window"] )
        csvFile.write( "%d, " % row["ui_method"] )
        csvFile.write( "%d, " % row["tab_site_hash"] )
        csvFile.write( "%d, " % row["num_tabs"] )
        csvFile.write( "%d, " % row["timestamp"] )
        if rowNum < len(extensions):
            csvFile.write("%s, " % extensions[rowNum])
        else:
            csvFile.write(",")
        if rowNum == 0:
            csvFile.write("%s, %s, %s" % ( pyObj["location"], pyObj["version"], pyObj["operatingSystem"] ) )
        else:
            csvFile.write(",,")
        csvFile.write("\n")
        rowNum += 1
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python json-to-csv.py infile outfile"
        sys.exit(1)

    inpath = sys.argv[1]
    outpath = sys.argv[2]
    outfilename = os.path.join( outpath, os.path.split( inpath )[1])
    print "Converting %s to %s." % (inpath, outfilename)

    try:
        f = open(inpath, 'r')
        text = f.read()
        f.close()
        pyObj = simplejson.loads(text)
        f2 = open(outfilename, 'w')
        pyDictToCsv(pyObj, f2)
        f2.close()
    except:
        print "File unparsable, skipping."
        sys.exit(1)
