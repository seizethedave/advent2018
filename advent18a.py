import copy
from collections import Counter
from itertools import chain

ITERS = 10

OPEN = "."
TREES = "|"
LUMBERYARD = "#"

def get_input():
    grid = []
    with open("advent18.txt", "r") as f:
        for line in f:
            grid.append(list(line.rstrip("\n")))
    return grid

def transform(grid, grid_orig, transform_from, transform_to, predicate):
    counter = Counter()

    for y, row in enumerate(grid_orig):
        for x, char in enumerate(row):
            if char != transform_from:
                continue

            counter.clear()

            for dx, dy in [
                    (-1, -1), (+0, -1), (+1, -1),
                    (-1, +0),           (+1, +0),
                    (-1, +1), (+0, +1), (+1, +1)]:
                if 0 <= x + dx < len(row) and 0 <= y + dy < len(grid_orig):
                    counter[grid_orig[y + dy][x + dx]] += 1

            if predicate(counter[OPEN], counter[TREES], counter[LUMBERYARD]):
                grid[y][x] = transform_to

def print_grid(grid):
    for row in grid:
        print "".join(row)
    print ""

def go():
    grid = get_input()

    for i in range(ITERS):
        grid_orig = copy.deepcopy(grid)

        transform(
            grid, grid_orig,
            OPEN, TREES,
            lambda num_open, num_trees, num_lumberyards: num_trees >= 3
        )

        transform(
            grid, grid_orig,
            TREES, LUMBERYARD,
            lambda num_open, num_trees, num_lumberyards: num_lumberyards >= 3
        )

        transform(
            grid, grid_orig,
            LUMBERYARD, OPEN,
            lambda num_open, num_trees, num_lumberyards: num_lumberyards == 0 or num_trees == 0
        )

    resource_counter = Counter(chain.from_iterable(grid))
    print resource_counter[TREES] * resource_counter[LUMBERYARD]

if __name__ == "__main__":
    go()
