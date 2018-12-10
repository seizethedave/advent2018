
from collections import defaultdict

def lines():
    with open('advent02.txt', 'r') as f:
        for line in f:
            yield line

def checksums():

    for line in lines():
        counter = defaultdict(int)
        for char in line:
            counter[char] += 1

        twos = 0
        threes = 0

        for char, count in counter.iteritems():
            if count == 2:
                twos = 1
            elif count == 3:
                threes = 1

        yield twos, threes


def go():
    twos = 0
    threes = 0

    for t2, t3 in checksums():
        twos += t2
        threes += t3

    print twos * threes

if __name__ == "__main__":
    go()
