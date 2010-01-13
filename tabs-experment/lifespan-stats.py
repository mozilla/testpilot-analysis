from math import sqrt

f = open("lifespans.dat", "r")

lifespans = f.readlines()

# square root of average value of square of deviation

lifespan_nums = [ long(lifespan) for lifespan in lifespans]

total = 0

for num in lifespan_nums:
    total += num

mean = total / len(lifespan_nums)

print "Mean is %d minutes." % ( mean / (1000 * 60) )

total = 0
for num in lifespan_nums:
    deviation = num - mean
    sq_dev = deviation * deviation
    total += sq_dev

mean_square_dev = total / len(lifespan_nums)

print "Std_dev is %d minutes." % (sqrt(mean_square_dev) / (1000 * 60))

print "Sorting..."
sorted_lifespans = sorted(lifespan_nums)
print "Median is %d minutes." % (sorted_lifespans[ int(len(sorted_lifespans)/2)] / (1000 * 60))
