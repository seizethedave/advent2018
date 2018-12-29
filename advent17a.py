import itertools

SPRING_X = None
SPRING_Y = 0

MIN_Y = None
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
        self.is_active = True

    @property
    def display_char(self):
        return LIQUID_ACTIVE if self.is_active else LIQUID_REST

def is_solid(x, y, grid):
    cell = grid[y][x]
    return cell is CLAY or (isinstance(cell, Drop) and not cell.is_active)

def flow_horizontal(x, y, grid):
    def flow_horizontal_dir(x, stride):
        # Returns x-coordinate of encountered clay wall, if any.
        while True:
            if grid[y][x] is EMPTY:
                grid[y][x] = Drop(x, y)

                if grid[y + 1][x] is EMPTY:
                    flow_drop(x, y + 1, grid)

                    if not is_solid(x + stride, y + 1, grid):
                        # Doing the drop-flow below didn't extend for us to continue horizontally. Stop looking.
                        return None
            elif grid[y][x] is CLAY:
                return x
            elif isinstance(grid[y][x], Drop):
                assert False

            x += stride

    left_wall_pos = flow_horizontal_dir(x - 1, stride=-1)
    right_wall_pos = flow_horizontal_dir(x + 1, stride=+1)

    if left_wall_pos is not None and right_wall_pos is not None:
        # Make the liquid solid.
        for cell in grid[y][left_wall_pos + 1:right_wall_pos]:
            assert isinstance(cell, Drop) and cell.is_active, y
            cell.is_active = False

def flow_drop(x, y, grid):
    """
    Drop down until encountering a non-empty space. Then take action there.
    """
    start_y = y

    while y <= MAX_Y:
        cell = grid[y][x]

        if cell is EMPTY:
            grid[y][x] = Drop(x, y)
        elif cell is CLAY:
            break
        elif isinstance(cell, Drop):
            if cell.is_active:
                # Dropping onto active liquid -- since flow is infinite, stop.
                return
            else:
                break # resting drop

        y += 1

    # Now we've hit solid ground. Flow horizontally and continue upwards while still solid.

    while is_solid(x, y, grid) and y > start_y:
        y -= 1
        flow_horizontal(x, y, grid)

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

def print_grid_row(row):
    print "".join(cell.display_char for cell in row)

def print_grid(grid, y=0):
    for row in grid[max(0, y-30):min(len(grid), y + 30)]:
        print_grid_row(row)

def print_grid_all(grid):
    for row in grid:
        print_grid_row(row)

def count_water(grid):
    return sum(
        1 for _ in itertools.ifilter(
            lambda cell: isinstance(cell, Drop),
            itertools.chain.from_iterable(itertools.islice(grid, MIN_Y, MAX_Y + 1))
        )
    )

def parse_grid():
    """
    Returns a grid filled with the items specified in the input file.
    This grid only contains the important part of the input, width-wise.
    """
    min_x = 50000
    max_x = -50000
    min_y = 50000
    max_y = -50000

    # Include some extra buffer space in both axes.
    BUF_X = 10
    BUF_Y = 10

    for x, y in iter_inputs():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    grid = [
        [EMPTY] * (max_x - min_x + 2 * BUF_X)
        for _ in xrange(max_y + BUF_Y)
    ]

    for x, y in iter_inputs():
        grid[y][x - min_x + BUF_X] = CLAY

    global SPRING_X
    SPRING_X = 500 - min_x + BUF_X
    global MIN_Y, MAX_Y
    MIN_Y = min_y
    MAX_Y = max_y

    return grid

def go():
    grid = parse_grid()
    flow_drop(SPRING_X, SPRING_Y, grid)
    # print_grid_all(grid)
    print count_water(grid)

if __name__ == "__main__":
    go()
