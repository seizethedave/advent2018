import heapq
from collections import namedtuple
import time

SPRING_X = None
SPRING_Y = 0

MAX_Y = None

LIQUID_ACTIVE = "|"
LIQUID_REST = "~"

class Clay(object):
    def __init__(self):
        self.display_char = "#"

class Empty(object):
    def __init__(self):
        self.display_char = "."

CLAY = Clay()
EMPTY = Empty()

class Drop(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.display_char = "|"

    def __lt__(self, other):
        return (MAX_Y - self.y, self.x) < (MAX_Y - other.y, other.x)

    def flow(self, grid):
        if grid[self.y + 1][self.x] == EMPTY:
            grid[self.y][self.x] = EMPTY
            self.y += 1
            grid[self.y][self.x] = self
            return True
        else:
            # Do nothing.
            return False

def iter_inputs():
    with open("advent17-test.txt", "r") as f:
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
    for row in grid[:50]:
        print "".join(cell.display_char for cell in row)

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
    global MAX_Y
    MAX_Y = max_y

    return grid

def flow_horizontal(x, y, grid):
    seen = set()

    def flow_inner(x):
        if x in seen:
            return None
        seen.add(x)
        print seen

        item = grid[y][x]

        if item is EMPTY:
            return x
        elif item is CLAY:
            return None
        elif isinstance(item, Drop):
            # Try to move it.
            new_x = flow_inner(x - 1)

            if new_x is None:
                new_x = flow_inner(x + 1)

            if new_x is not None:
                grid[item.y][item.x] = EMPTY
                item.x = new_x
                grid[item.y][item.x] = item
                return x
            else:
                return None
        else:
            assert False

    return flow_inner(x)

def go():
    grid = parse_grid()
    print_grid(grid)

    active_water = []
    did_change = True
    i = 0

    while did_change:
        i += 1
        did_change = False
        new_drop = Drop(SPRING_X, SPRING_Y)
        heapq.heappush(active_water, new_drop)
        # assert grid[SPRING_Y][SPRING_X] is EMPTY
        grid[SPRING_Y][SPRING_X] = new_drop
        next_active_water = []

        while active_water:
            drop = heapq.heappop(active_water)
            did_flow = drop.flow(grid)

            if not did_flow and grid[drop.y + 1][drop.x] is CLAY:
                f = flow_horizontal(drop.x, drop.y, grid)
                did_flow = f is not None

            if did_flow:
                did_change = True

            heapq.heappush(next_active_water, drop)

        active_water = next_active_water
        print i
        print_grid(grid)
        time.sleep(1/20.0)

if __name__ == "__main__":
    go()
