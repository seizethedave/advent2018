import heapq
from collections import namedtuple
import time

SPRING_X = None
SPRING_Y = 0

EMPTY = "."
CLAY = "#"
LIQUID_ACTIVE = "|"
LIQUID_REST = "~"

Drop = namedtuple("Drop", ('x', 'y'))

class Drop(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        return (self.y, self.x) >= (other.y, other.x)


def iter_inputs():
    with open("advent17.txt", "r") as f:
        for line in f:
            left, right = line.split(", ")
            x_major = left.startswith("x=")
            major = int(left[2:])
            minor_range = right[2:].split("..")
            minor_from = int(minor_range[0])
            minor_to = int(minor_range[1])

            for minor in xrange(minor_from, minor_to + 1):
                yield (major, minor)[::1 if x_major else -1]

def print_grid(grid):
    for row in grid[:100]:
        print "".join(row)
    print ""

def parse_grid():
    min_x = 50000
    max_x = -50000
    min_y = 50000
    max_y = -50000
    BUF_X = 10

    for x, y in iter_inputs():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    grid = [
        [EMPTY] * (max_x - min_x + 2 * BUF_X)
        for _ in xrange(max_y + 1)
    ]

    for x, y in iter_inputs():
        grid[y][x - min_x + BUF_X] = CLAY

    global SPRING_X
    SPRING_X = 500 - min_x + BUF_X

    return grid

def go():
    grid = parse_grid()
    print_grid(grid)

    active_water = []
    did_change = True

    def drop_flow(drop):
        if grid[drop.y + 1][drop.x] == EMPTY:
            return Drop(drop.x, drop.y + 1)
        elif grid[drop.y][drop.x - 1] == EMPTY:
            return Drop(drop.x - 1, drop.y)
        elif grid[drop.y][drop.x + 1] == EMPTY:
            return Drop(drop.x + 1, drop.y)
        else:
            # Do nothing.
            return drop

    while did_change:
        did_change = False
        heapq.heappush(active_water, Drop(SPRING_X, SPRING_Y))
        grid[SPRING_Y][SPRING_X] = LIQUID_ACTIVE

        next_active_water = []

        while active_water:
            drop = heapq.heappop(active_water)
            flowed_drop = drop_flow(drop)

            if drop != flowed_drop:
                grid[drop.y][drop.x] = EMPTY
                grid[flowed_drop.y][flowed_drop.x] = LIQUID_ACTIVE
                did_change = True

            heapq.heappush(next_active_water, flowed_drop)

        active_water = next_active_water
        print_grid(grid)
        time.sleep(1/20.0)

if __name__ == "__main__":
    go()
