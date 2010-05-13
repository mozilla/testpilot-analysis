import os
import sys
import hashlib
import random

known_extensions = {
  "{89506680-e3f4-484c-a2c0-ed711d481eda}": "Firefox showcase",
  "firegestures@xuldev.org": "Fire gestures",
  "{ef4e370e-d9f0-4e00-b93e-a4f274cfdd5a}": "Fox Tab",
  "multipletab@piro.sakura.ne.jp": "Multiple Tab Handler",
  "quickdrag@mozilla.ktechcomputing.com": "Quick Drag",
  "{dc572301-7619-498c-a57d-39143191b318}": "Tab Mix Plus",
  "tabscope@xuldev.org": "Tab Scope",
  "tabsopenrelative@jomel.me.uk": "Tab Open Relative",
  "treestyletab@piro.sakura.ne.jp": "Tree Style Tab"
}


def hash_sha1(input):
    m = hashlib.sha1()
    m.update(input)
    return m.hexdigest()

BAD_EXTS = [ hash_sha1(x) for x in known_extensions.keys()]

def hasBadExtensions(extensionList):
    for ext in extensionList:
        if ext in BAD_EXTS:
            return True
    return False


HEADER = "user, os, fx_version, event_code, tab_id, tab_position, tab_window, ui_method, tab_site_hash, is_search_results, num_tabs, timestamp"


FILENAME = "tab-switch-study-aggregated-%d.csv"
print "Will write to tab-switch-study-aggregated.csv"
outfiles = [open( FILENAME % x, "w") for x in range(4)]

for outfile in outfiles:
    outfile.write( HEADER )

rootdir = "/var/testpilot/storage/5"

user_num = 0
filenames = os.listdir(rootdir)

for filename in filenames:
    # Skip all the header stuff
    # Pull out the extensions, compare to list of known-bad extensions.
    filename = os.path.join( rootdir, filename.strip("\n") )
    outfile = outfiles[ user_num % 4 ]
    print "Processing %s to outfile %d" % (filename, user_num % 4)

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
    if hasBadExtensions(extensions):
        print "Has one of the forbidden extensions."
        continue
    numExtensions = len( extensions )
    locale = metadata[3]

    headerIsOver = False
    for line in lines:
        # skip headers:
        if not headerIsOver:
            # In the header
            if "event_code, tab_id, tab_position" in line:
                headerIsOver = True
            continue

        outfile.write( "%d, %s, %s, %s\n" % ( user_num, OS, fxVersion, line.strip("\n") ) )

    user_num += 1

for outfile in outfiles:
    outfile.close()
