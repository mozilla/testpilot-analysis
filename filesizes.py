import os
import sys
import datetime

rootdir = sys.argv[1]

print "Looking at files in %s." % rootdir

tot = 0L
num = 0

datePiles = [0] * 13
sizes = []

for file in os.listdir(rootdir):
    path = os.path.join( rootdir, file )
    stat = os.stat(path)
    size = stat.st_size
    date = datetime.date.fromtimestamp(stat.st_mtime)
    month = date.month
    day = date.day
    if datePiles[month] == 0:
        datePiles[month] = [0] * 32
    datePiles[month][day] += 1
    tot += size
    num += 1
    sizes.append(size)
    

sizes.sort()

min = sizes[0]
max = sizes[-1]
median = sizes[ num / 2 ]
first_quart = sizes[ num / 4 ]
third_quart = sizes[ 3 * num / 4]

print "Number of files: %d." % num
print "Min size: %d bytes" % min
print "First quartile: %d bytes" % first_quart
print "Mean size: %d bytes" % (tot / num)
print "Median size: %d bytes" % median
print "Third quartile: %d bytes" % third_quart
print "Max size: %d bytes" % max

for m in range( len(datePiles) ):
    if datePiles[m] != 0:
        for d in range( len(datePiles[m]) ):
            if datePiles[m][d] != 0:
                print "Month %d, day %d: %d submissions" % (m, d, datePiles[m][d])

