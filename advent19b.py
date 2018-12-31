import math

target = 10551428
count = 0

for i in xrange(1, int(math.ceil(math.sqrt(target))) + 1):
    other = target // i
    if i * other == target:
        print i, other
        count += i + other

print count
