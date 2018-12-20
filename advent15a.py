import heapq
import itertools
import pprint

ATTACK_POWER = 3

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

def adjacent_squares(x, y):
    return [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]

def open_adjacent_squares(x, y, grid):
    return itertools.ifilter(
        lambda (x_, y_): grid[y_][x_] is OPEN,
        [(x, y - 1), (x - 1, y), (x + 1, y), (x, y + 1)]
    )

def closest_target(source, targets, grid):
    x, y = source
    fringe = [(0, (y, x), None, ((y, x),))]
    seen = set()
    nearest_distance = None
    nearest = []

    while fringe:
        dist, (y, x), parent, this_path = heapq.heappop(fringe)
        #seen.add((y, x))

        if nearest_distance is not None and dist > nearest_distance:
            # Already found something closer. Don't bother.
            continue

        if (y, x) in targets:
            if nearest_distance is None:
                nearest_distance = dist
                nearest.append(((y, x), this_path))
            elif nearest_distance == dist:
                nearest.append(((y, x), this_path))
            # Cannot beat this distance by traveling through this target square.
            continue

        for (nextX, nextY) in open_adjacent_squares(x, y, grid):
            if (nextY, nextX) not in seen:
                seen.add((nextY, nextX))
                item = (dist + 1, (nextY, nextX), (y, x), this_path + ((nextY, nextX),))
                heapq.heappush(fringe, item)

    # min(nearest) is the first one in there, reading-order wise.

    if not nearest:
        return None, None

    return min(nearest)

class Player(object):
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.hit_points = 200
        self.alive = True

    def get_targets(self):
        return itertools.ifilter(
            lambda p: not isinstance(p, type(self)),
            iter_players(self.grid)
        )

    def attackable_targets(self):
        enemy_type = Goblin if isinstance(self, Elf) else Elf

        for x, y in adjacent_squares(self.x, self.y):
            if isinstance(self.grid[y][x], enemy_type):
                yield (self.grid[y][x].hit_points, (y, x))

    def play_turn(self):
        def iter_reachable_squares():
            for target in self.get_targets():
                for (x, y) in open_adjacent_squares(target.x, target.y, self.grid):
                    yield (y, x)

        had_enemies = any(self.get_targets())

        if len(list(self.attackable_targets())) == 0:
            # Need to move.
            in_range_squares = set(iter_reachable_squares())
            closest_in_range, path = closest_target(
                (self.x, self.y), in_range_squares, self.grid)
            # print (self.y, self.x), "->", (closest_in_range)
            # print "  path was", path

            # Take one step toward the closest.
            if closest_in_range is not None:
                self.move_to(path[1])

        attackable_targets = list(self.attackable_targets())

        if attackable_targets:
            health, targetPosition = min(attackable_targets)
            self.attack(targetPosition)

        return had_enemies

    def move_to(self, position):
        y, x = position
        assert self.grid[y][x] is OPEN
        self.grid[self.y][self.x] = OPEN
        self.grid[y][x] = self
        self.y = y
        self.x = x

    def attack(self, position):
        targetY, targetX = position
        target = self.grid[targetY][targetX]
        target.hit_points -= ATTACK_POWER
        if target.hit_points <= 0:
            target.alive = False
            self.grid[targetY][targetX] = OPEN

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

def iter_elves(grid):
    return itertools.ifilter(
        lambda p: isinstance(p, Elf),
        itertools.chain.from_iterable(grid)
    )

def iter_goblins(grid):
    return itertools.ifilter(
        lambda p: isinstance(p, Goblin),
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

    rounds_completed = 0

    while True:
        for player in list(iter_players(grid)):
            if player.alive:
                had_enemies = player.play_turn()
                if not had_enemies:
                    break
        else:
            rounds_completed += 1

        print rounds_completed
        debug_grid(grid)

        elves = list(iter_elves(grid))
        goblins = list(iter_goblins(grid))

        if not elves:
            print rounds_completed * sum(g.hit_points for g in goblins)
            break
        elif not goblins:
            print rounds_completed * sum(e.hit_points for e in elves)
            break

if __name__ == "__main__":
    go()
