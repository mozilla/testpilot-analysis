import os
import os.path
import hashlib
import sys

locales = {}
oses = {}
versions = {}

extensions = {}

num_extensions_per_user = {}

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

one_extension_filez = {}
for ext_id in known_extensions.keys():
    hash = hash_sha1(ext_id)
    extensions[ hash ] = 0
    one_extension_filez[ hash ] = { "called": known_extensions[ext_id].replace(" ", "_"),
                                    "contents": [] }

rootdir = "/var/www/testpilot/storage/1-csv"

mac_filenames = []
windows_filenames = []
linux_filenames = []
no_ext_filenames = []


for file in os.listdir(rootdir):
    path = os.path.join( rootdir, file )
    f = open(path, "r")
    header = f.readline()
    firstline = f.readline()
    cells = firstline.split(",")
    locale = cells[8].strip(" ")
    version = cells[9].strip(" ")
    myos = cells[10].strip("\n")
    if "Linux" in myos:
        linux_filenames.append( path )
    elif "Windows" in myos:
        windows_filenames.append( path )
    elif "Mac" in myos:
        mac_filenames.append( path )
    myextensions = []
    while len(firstline) > 0:
        cells = firstline.split(",")
        if len( cells[7].strip(" ") ) > 0:
            myextensions.append( cells[7].strip(" ") )
        firstline = f.readline()

    if locales.has_key(locale):
        locales[locale] += 1
    else:
        locales[locale] = 1

    if oses.has_key(myos):
        oses[myos] += 1
    else:
        oses[myos] = 1

    if versions.has_key(version):
        versions[version] += 1
    else:
        versions[version] = 1

    my_num_tabs_extensions = 0
    for ext in myextensions:
        if extensions.has_key( ext ):
            extensions[ext] += 1
            my_num_tabs_extensions += 1

    if num_extensions_per_user.has_key( my_num_tabs_extensions ):
        num_extensions_per_user[my_num_tabs_extensions ] += 1
    else:
        num_extensions_per_user[my_num_tabs_extensions ] = 1

    if my_num_tabs_extensions == 0:
        no_ext_filenames.append( path )
    elif my_num_tabs_extensions == 1:
        for ext in extensions.keys():
            if ext in myextensions:
                one_extension_filez[ext]["contents"].append(path)

    f.close()

print "Locales:"
print locales
print "Operating systems:"
print oses
print "Versions:"
print versions

print "Number of each extension:"
for ext_id in known_extensions.keys():
    print known_extensions[ext_id], " : ", extensions[ hash_sha1(ext_id) ]

print "Extensions per user:"
print num_extensions_per_user

for ext in extensions.keys():
    outfile = open( one_extension_filez[ext]["called"] + "_filenames.dat", "w")
    for file in one_extension_filez[ext]["contents"]:
        outfile.write("%s\n" % file )
    outfile.close()

#outfile = open("windows-users-filenames.dat", "w")
#for file in windows_filenames:
#    outfile.write("%s\n" % file)
#outfile.close()

#outfile = open("mac-users-filenames.dat", "w")
#for file in mac_filenames:
#    outfile.write("%s\n" % file)
#outfile.close()

#outfile = open("linux-users-filenames.dat", "w")
#for file in linux_filenames:
#    outfile.write("%s\n" % file)
#outfile.close()

#outfile = open("no-ext-filenames.dat", "w")
#for file in no_ext_filenames:
#    outfile.write("%s\n" % file)
#outfile.close()
