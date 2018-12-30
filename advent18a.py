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
    for y, row in enumerate(grid_orig):
        for x, char in enumerate(row):
            if char != transform_from:
                continue

            counter = Counter()

            for dx, dy in [
                    (-1, -1), (+0, -1), (+1, -1),
                    (-1, +0),           (+1, +0),
                    (-1, +1), (+0, +1), (+1, +1)]:
                if 0 <= x + dx < len(row) and 0 <= y + dy < len(grid_orig):
                    counter[grid_orig[y + dy][x + dx]] += 1

            if predicate(counter[OPEN], counter[TREES], counter[LUMBERYARD]):
                grid[y][x] = transform_to

def resource_value(grid):
    trees = 0
    lumber = 0

    for char in chain.from_iterable(grid):
        if char == TREES:
            trees += 1
        elif char == LUMBERYARD:
            lumber += 1

    return trees * lumber

def print_grid(grid):
    for row in grid:
        print "".join(row)
    print ""

def go():
    grid = get_input()
    print_grid(grid)

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

        print_grid(grid)

    print resource_value(grid)

if __name__ == "__main__":
    go()
