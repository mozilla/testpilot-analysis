import os

user_num = 0

rootdir = "/var/www/testpilot/storage/4"

def hasBadExtensions(extList):
    BAD_EXTS = ["a8e3b43c6762d939c7b0cca8841ad15f1225071f", "04b74bb753460d89360e3559df681e585775d248", "30b61e2044b78e9837fb12ec30520497cf940d87", "5c35c27a7aa4e199cef01277a8dd457092faa719", "9ae23e629db96d0393341111ab230f17ab8f0506", "30bc235d1021b4de339714fe994f639cc5e1bfda", "63ac0216c67bafc7978c6e53fd3ca457084b5b57"]
    for ext in extList:
        if ext in BAD_EXTS:
            return True
    return False

os_stats = {}
fxVersion_stats = {}
extensions_stats = {}
locale_stats = {}

for file in os.listdir(rootdir):
    path = os.path.join( rootdir, file )
    
    #print "Processing %s." % path
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    metadata = lines[1].split(",")
    fxVersion = metadata[0]
    OS = metadata[4].strip("\n")
    extensions = lines[3].split(",")
    if hasBadExtensions(extensions):
        print "Has one of the forbidden extensions."
        continue
    numExtensions = len( extensions )
    locale = metadata[3]

    print "Processing %s ; locale is %s." % ( file, locale )

    if os_stats.has_key(OS):
        os_stats[OS] += 1
    else:
        os_stats[OS] = 1

    if fxVersion_stats.has_key( fxVersion ):
        fxVersion_stats[fxVersion] += 1
    else:
        fxVersion_stats[fxVersion] = 1

    if extensions_stats.has_key(numExtensions):
        extensions_stats[numExtensions] += 1
    else:
        extensions_stats[numExtensions] = 1

    if locale_stats.has_key(locale):
        locale_stats[locale] += 1
    else:
        locale_stats[locale] = 1


print "Operating system, Number"
for key in os_stats.keys():
    print "%s , %d" % ( key, os_stats[key])
print "Firefox version, Number "
for key in fxVersion_stats.keys():
    print "%s , %d" % ( key, fxVersion_stats[key])
print "Number of extensions, Number of users"
for key in extensions_stats.keys():
    print "%s , %d" % ( key, extensions_stats[key])
print "Locale, Number"
for key in locale_stats.keys():
    print "%s , %d" % ( key, locale_stats[key])
