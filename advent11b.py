import itertools
import pprint

SERIAL = 9424
SIZE = 300

def cell_power(x, y):
    rack = x + 10
    power = ((rack * y) + SERIAL) * rack
    return ((power // 100) % 10) - 5

def go():
    best_sum = 0
    grid = []

    for y in xrange(SIZE):
        grid.append([cell_power(x + 1, y + 1) for x in xrange(SIZE)])

    for square_size in xrange(1, SIZE + 1):
        # Compute sum of square at 0,0. Then change the sum one column or row at a time.

        for row in xrange(0, SIZE + 1 - square_size):
            square_sum = sum(
                grid[y][x]
                for x, y in itertools.product(
                    xrange(0, square_size),
                    xrange(row, row + square_size)
                )
            )

            if square_sum > best_sum:
                best_sum = square_sum
                print "{},{},{}  ({})".format(1, row + 1, square_size, square_sum)

            for col in xrange(1, SIZE + 1 - square_size):
                square_sum += sum(
                    grid[y][col + square_size - 1] - grid[y][col - 1]
                    for y in xrange(row, row + square_size)
                )

                if square_sum > best_sum:
                    best_sum = square_sum
                    print "{},{},{}  ({})".format(col + 1, row + 1, square_size, square_sum)


if __name__ == "__main__":
    go()
