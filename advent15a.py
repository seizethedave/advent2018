import heapq
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

def reachable(source, dest, grid):
    return True

def open_adjacent_squares(x, y, grid):
    return itertools.ifilter(
        lambda (x_, y_): grid[y_][x_] is OPEN,
        [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    )

def closest_target(source, targets, grid):
    x, y = source
    fringe = [(0, (y, x))]
    seen = set()
    nearest_distance = None
    nearest = set()

    while fringe:
        dist, (y, x) = heapq.heappop(fringe)
        seen.add((y, x))

        if nearest_distance is not None and dist > nearest_distance:
            # Already found something closer. Don't bother.
            continue

        if (y, x) in targets:
            if nearest_distance is None:
                nearest_distance = dist
                nearest.add((y, x))
            elif nearest_distance == dist:
                nearest.add((y, x))
            # Cannot beat this distance by traveling through this target square.
            continue

        for (nextX, nextY) in open_adjacent_squares(x, y, grid):
            if (nextY, nextX) not in seen:
                item = (dist + 1, (nextY, nextX))
                heapq.heappush(fringe, item)

    # min(nearest) is the first one in there, reading-order wise.
    return min(nearest)

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
                for (x, y) in open_adjacent_squares(target.x, target.y, self.grid):
                    if reachable(x, y, self.grid):
                        yield (y, x)

        in_range_squares = set(iter_reachable_squares())
        closest_in_range = closest_target(
            (self.x, self.y), in_range_squares, self.grid)
        print (self.y, self.x), "->", (closest_in_range)

        # Take one step toward the closest.

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
