target = 10551428
count = 0

for i in xrange(1, target + 1):
    other = target // i
    if i * other == target:
        print i, other
        count += i

print count
