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
    for row in grid:
        print "".join(row)

def go():
    min_x = 50000
    max_x = -50000
    min_y = 50000
    max_y = -50000

    for x, y in iter_inputs():
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    grid = [
        [' '] * (max_x + 1)
        for _ in xrange(max_y + 1)
    ]

    for x, y in iter_inputs():
        grid[y][x] = "#"

    print_grid(grid)

if __name__ == "__main__":
    go()
