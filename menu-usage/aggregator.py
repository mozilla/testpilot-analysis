import os
import sys
import random

HEADER = "user, os, fx_version, ui_method, start_menu_id, explore_ms, explore_num, menu_id, item_id, timestamp\n"

user_num = 0

outfile = open("menu-item-usage-70.csv" , 'w')
outfile.write(HEADER)

rootdir = "/var/www/testpilot/storage/4"

def hasBadExtensions(extList):
    BAD_EXTS = ["a8e3b43c6762d939c7b0cca8841ad15f1225071f", "04b74bb753460d89360e3559df681e585775d248", "30b61e2044b78e9837fb12ec30520497cf940d87", "5c35c27a7aa4e199cef01277a8dd457092faa719", "9ae23e629db96d0393341111ab230f17ab8f0506", "30bc235d1021b4de339714fe994f639cc5e1bfda", "63ac0216c67bafc7978c6e53fd3ca457084b5b57"]
    for ext in extList:
        if ext in BAD_EXTS:
            return True
    return False


def interpretItemId(id):
    if id == 0: return "New Window"
    elif id == 1: return "New Tab"
    elif id == 2: return "Open Location"
    elif id == 3: return "Open File"
    elif id == 4: return "Close Window"
    elif id == 5: return "Close Tab"
    elif id == 6: return "Save Page As"
    elif id == 7: return "Send Link"
    elif id == 8: return "Page Setup"
    elif id == 9: return "Print Preview"
    elif id == 10: return "Print"
    elif id == 11: return "Import"
    elif id == 12: return "Work Offline"
    elif id == 13: return "Exit"
    elif id == 14: return "Undo"
    elif id == 15: return "Redo"
    elif id == 16: return "Cut"
    elif id == 17: return "Paste"
    elif id == 18: return "Copy"
    elif id == 19: return "Delete"
    elif id == 20: return "Select All"
    elif id == 21: return "Find"
    elif id == 22: return "Find Again"
    elif id == 23: return "Special Characters"
    elif id == 24: return "Toolbars"
    elif id == 25: return "Toolbars/Customize"
    elif id == 26: return "Status Bar"
    elif id == 27: return "Sidebar/Bookmarks"
    elif id == 28: return "Sidebar/History"
    elif id == 29: return "Stop"
    elif id == 30: return "Reload"
    elif id == 31: return "Zoom In"
    elif id == 32: return "Zoom Out"
    elif id == 33: return "Zoom/Reset"
    elif id == 34: return "Zoom Text Only"
    elif id == 35: return "Page Style/No Style"
    elif id == 36: return "Page Style/Basic Page Style"
    elif id == 37: return "Character Encoding/Autodetect/*"
    elif id == 38: return "Character Encoding/More Encodings/*"
    elif id == 39: return "Character Encoding/Customize List"
    elif id == 40: return "Character Encoding/Western"
    elif id == 41: return "Character Encoding/UTF-16"
    elif id == 42: return "View Source"
    elif id == 43: return "Full Screen"
    elif id == 44: return "Back"
    elif id == 45: return "Forward"
    elif id == 46: return "Home"
    elif id == 47: return "Show All History"
    elif id == 48: return "(User History Item)"
    elif id == 49: return "Recently Closed Tab"
    elif id == 50: return "Restore All Tabs"
    elif id == 51: return "Recently Closed Window"
    elif id == 52: return "Restore All Windows"
    elif id == 53: return "Bookmark This Page"
    elif id == 54: return "Subscribe to This Page"
    elif id == 55: return "Bookmark All Tabs"
    elif id == 56: return "Organize Bookmarks"
    elif id == 57: return "(User Bookmark Item)"
    elif id == 58: return "Web Search"
    elif id == 59: return "Downloads"
    elif id == 60: return "Add-Ons"
    elif id == 61: return "Error Console"
    elif id == 62: return "Page Info"
    elif id == 63: return "Private Browsing"
    elif id == 64: return "Clear Recent History"
    elif id == 65: return "Options"
    elif id == 66: return "Minimize"
    elif id == 67: return "Zoom"
    elif id == 68: return "(User Window)"
    elif id == 69: return "Firefox Help"
    elif id == 70: return "For Internet Explorer Users"
    elif id == 71: return "Troubleshooting Information"
    elif id == 72: return "Release Notes"
    elif id == 73: return "Report Broken Web Site"
    elif id == 74: return "Report Web Forgery"
    elif id == 75: return "Check for Updates"
    elif id == 76: return "About Mozilla Firefox"
    return "Unknown"

def interpretMenuId(id):
    return ["File", "Edit", "View", "History", "Bookmarks", "Tools", "Windows", "Help"][id]


commonMisfires = []

def addToCommonMisfires(start_menu_id, menu_id, item_id, explore_ms, explore_num):
    if explore_ms == 0 and explore_num == 0:
        return
    for x in commonMisfires:
        if x["start_menu_id"] == start_menu_id and x["menu_id"] == menu_id and x["item_id"] == item_id:
            x["count"] += 1
            x["total_ms"] += explore_ms
            x["total_num"] += explore_num
            return
    commonMisfires.append( { "start_menu_id": start_menu_id, "menu_id": menu_id, "item_id": item_id, "count": 1, "total_ms": explore_ms, "total_num": explore_num } )


def makeSubSample(percent):
    dataLines = os.listdir(rootdir)
    print "There are %d files total." % len(dataLines)
    print "Generating %d\ percent sample." % percent
    print "Shuffling..."
    random.shuffle(dataLines)

    n = int( len(dataLines) * percent / 100)
    print "Selecting %d percent, or %d." % (percent, n)

    subSample = dataLines[:n]
    return subSample


for file in makeSubSample(70):
    path = os.path.join( rootdir, file )
    
    #print "Processing %s." % path
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    metadata = lines[1].split(",")
    fxVersion = metadata[0]
    OS = metadata[4].strip("\n")
    if "ja" in OS:
        continue
    #if "WIN" in OS or "Win" in OS or "win" in OS:
    #    pass
    #else:
    #    continue
    extensions = lines[3].split(",")
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
            if "start_menu_id, explore_ms" in line:
                headerIsOver = True
            continue

        # take user number plus first six cells..
        #    print "file %s: OS is %s" % (file, OS)
        stuff = line.strip("\n").split(",")
        #ui_method, start_menu_id, explore_ms, explore_num, menu_id, item_id, timestamp
        ui_method = int(stuff[0])
        start_menu_id = int(stuff[1])
        menu_id = int(stuff[4])
        item_id = int(stuff[5])
        explore_ms = int(stuff[2])
        explore_num = int(stuff[3])
        #if ui_method == 0:
        #    if start_menu_id != menu_id:
        #        if menu_id != -3 and menu_id != -1 and item_id != -3 and item_id != -1:
        #            addToCommonMisfires(start_menu_id, menu_id, item_id, explore_ms, explore_num)
        #            #print "Explore_ms: %d, Explore_num: %d" % (explore_ms, explore_num)
        outfile.write( "%d, %s, %s, %s\n" % ( user_num, OS, fxVersion, line.strip("\n") ) )
    user_num += 1

outfile.close()

#misfiresFile = open("misfires.csv", "w")
#misfiresFile.write("start_menu_id, menu_id, item_id, count, avg_explore_ms, avg_explore_num\n")
#for x in commonMisfires:
#    misfiresFile.write( "%s, %s, %s, %d, %d, %d\n" % (interpretMenuId(x["start_menu_id"]), interpretMenuId(x["menu_id"]), interpretItemId(x["item_id"]), x["count"], x["total_ms"]/x["count"], x["total_num"]/x["count"] ))
#misfiresFile.close()

