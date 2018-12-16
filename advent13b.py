import itertools

DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

TURN_STRAIGHT = 0
TURN_LEFT = 1
TURN_RIGHT = 2

class Cart(object):
    def __init__(self, num, cursor, x, y, grid):
        self.num = num
        self.direction = {
            '^': DIR_UP,
            'v': DIR_DOWN,
            '<': DIR_LEFT,
            '>': DIR_RIGHT,
        }[cursor]

        self.x = x
        self.y = y
        self.turn_choices = itertools.cycle([TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT])
        self.grid = grid
        self.removed = False

    def turn(self):
        turn = next(self.turn_choices)

        if self.direction == DIR_UP:
            if turn == TURN_LEFT:
                self.direction = DIR_LEFT
            elif turn == TURN_RIGHT:
                self.direction = DIR_RIGHT
        elif self.direction == DIR_DOWN:
            if turn == TURN_LEFT:
                self.direction = DIR_RIGHT
            elif turn == TURN_RIGHT:
                self.direction = DIR_LEFT
        elif self.direction == DIR_LEFT:
            if turn == TURN_LEFT:
                self.direction = DIR_DOWN
            elif turn == TURN_RIGHT:
                self.direction = DIR_UP
        elif self.direction == DIR_RIGHT:
            if turn == TURN_LEFT:
                self.direction = DIR_UP
            elif turn == TURN_RIGHT:
                self.direction = DIR_DOWN

    def tick(self):
        if self.direction == DIR_UP:
            self.y -= 1
            if self.grid[self.y][self.x] == "/":
                self.direction = DIR_RIGHT
            elif self.grid[self.y][self.x] == "\\":
                self.direction = DIR_LEFT
            elif self.grid[self.y][self.x] == "+":
                self.turn()
        elif self.direction == DIR_DOWN:
            self.y += 1
            if self.grid[self.y][self.x] == "/":
                self.direction = DIR_LEFT
            elif self.grid[self.y][self.x] == "\\":
                self.direction = DIR_RIGHT
            elif self.grid[self.y][self.x] == "+":
                self.turn()
        elif self.direction == DIR_LEFT:
            self.x -= 1
            if self.grid[self.y][self.x] == "/":
                self.direction = DIR_DOWN
            elif self.grid[self.y][self.x] == "\\":
                self.direction = DIR_UP
            elif self.grid[self.y][self.x] == "+":
                self.turn()
        elif self.direction == DIR_RIGHT:
            self.x += 1
            if self.grid[self.y][self.x] == "/":
                self.direction = DIR_UP
            elif self.grid[self.y][self.x] == "\\":
                self.direction = DIR_DOWN
            elif self.grid[self.y][self.x] == "+":
                self.turn()

        assert self.grid[self.y][self.x] != ' '

    def __cmp__(self, other):
        if self is other:
            return 0
        return cmp((self.y, self.x), (other.y, other.x))

    @property
    def pos(self):
        return (self.x, self.y)

    def __repr__(self):
        direction_str = {
            DIR_UP: 'up',
            DIR_DOWN: 'down',
            DIR_LEFT: 'left',
            DIR_RIGHT: 'right',
        }[self.direction]
        return "<Cart {} facing {} at {}>".format(self.num, direction_str, (self.x, self.y))


def debug_grid(grid, carts):
    debug_grid = [list(line) for line in grid]

    for cart in carts:
        debug_grid[cart.y][cart.x] = "@"

    for i, line in enumerate(debug_grid, start=1):
        print "{:<5} {}".format(i, "".join(line))

def go():
    grid = []
    carts = []

    with open("advent13.txt", "r") as f:
        cart_num = 1
        for y, line in enumerate(f):
            line = line.rstrip("\n")
            grid.append(line)

            for x, char in enumerate(line):
                if char in '<>^v':
                    carts.append(Cart(cart_num, char, x, y, grid))
                    cart_num += 1

    while True:
        carts = filter(lambda c: not c.removed, carts)

        #debug_grid(grid, carts) ; _ = raw_input()

        if len(carts) == 1:
            print "{},{}".format(carts[0].x, carts[0].y)
            return

        carts.sort()

        for cart in carts:
            cart.tick()
            colliding_carts = [c for c in carts if c.pos == cart.pos]

            if len(colliding_carts) > 1:
                for other_cart in colliding_carts:
                    other_cart.removed = True

if __name__ == "__main__":
    go()
