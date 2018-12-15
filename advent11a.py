import itertools

SERIAL = 9424
SIZE = 300

def cell_power(x, y):
    rack = x + 10
    power = ((rack * y) + SERIAL) * rack
    return ((power // 100) % 10) + 5

def go():
    best_sum = 0
    grid = []

    for y in xrange(SIZE):
        grid.append([cell_power(x, y) for x in xrange(SIZE)])

    square_size = 3

    if True: #for square_size in xrange(SIZE, 0, -1):
        for row in xrange(0, SIZE + 1 - square_size):
            for col in xrange(0, SIZE + 1 - square_size):
                part_sum = sum(
                    grid[y][x]
                    for x, y in itertools.product(
                        xrange(col, col + square_size),
                        xrange(row, row + square_size)
                    )
                )

                if part_sum > best_sum:
                    best_sum = part_sum
                    print "{},{},{}  ({})".format(col, row, square_size, part_sum)

if __name__ == "__main__":
    go()
