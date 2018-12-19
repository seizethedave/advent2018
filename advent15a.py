import itertools

class Wall(object):
    @property
    def grid_char(self):
        return "#"

class Open(object):
    @property
    def grid_char(self):
        return "."

WALL = Wall()
OPEN = Open()

def reachable(_from, _to, grid):
    return True

def squares_in_range(x, y, grid):
    return filter(
        lambda (x_, y_): grid[y_][x_] is OPEN,
        [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    )

class Player(object):
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid

    def get_targets(self):
        return itertools.ifilter(
            lambda p: not isinstance(p, type(self)),
            iter_players(self.grid)
        )

    def play_turn(self):
        def iter_reachable_squares():
            for target in self.get_targets():
                for (x, y) in squares_in_range(target.x, target.y, self.grid):
                    if reachable(x, y, self.grid):
                        yield (x, y)

        print list(iter_reachable_squares())

    def move(self):
        pass

    def attack(self):
        pass

    def __repr__(self):
        return "<{} @ {}>".format(type(self), (self.x, self.y))

class Goblin(Player):
    @property
    def grid_char(self):
        return "G"

class Elf(Player):
    @property
    def grid_char(self):
        return "E"

def debug_grid(grid):
    for line in grid:
        print "".join(item.grid_char for item in line)

def iter_players(grid):
    return itertools.ifilter(
        lambda p: isinstance(p, Player),
        itertools.chain.from_iterable(grid)
    )

def go():
    grid = []

    with open("advent15.txt", "r") as f:
        for y, line in enumerate(f):
            line = line.rstrip("\n")
            grid_line = []
            for x, char in enumerate(line):
                if "#" == char:
                    grid_line.append(WALL)
                elif "." == char:
                    grid_line.append(OPEN)
                elif "G" == char:
                    grid_line.append(Goblin(x, y, grid))
                elif "E" == char:
                    grid_line.append(Elf(x, y, grid))
                else:
                    assert False
            else:
                grid.append(grid_line)

    debug_grid(grid)

    for player in iter_players(grid):
        print player
        player.play_turn()


if __name__ == "__main__":
    go()