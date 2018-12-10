from collections import Counter
import re

# #8 @ 256,742: 18x14

class Claim(object):
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def iter_coordinates(self):
        for y in xrange(self.y, self.y + self.height):
            for x in xrange(self.x, self.x + self.width):
                yield (x, y)

    def __repr__(self):
        return "<Claim id {}>".format(self.id)

def iter_claims():
    with open("advent03.txt", "r") as f:
        for line in f:
            yield Claim(*map(int, re.findall(r'\d+', line)))

def go():
    fabric = {}
    unseen = set()

    for claim in iter_claims():
        unseen.add(claim)

        for coordinate in claim.iter_coordinates():
            other = fabric.get(coordinate)

            if other is not None:
                unseen.discard(other)
                unseen.discard(claim)
            else:
                fabric[coordinate] = claim

    print unseen

if __name__ == "__main__":
    go()
