rules_str = """.#.## => .
...## => #
..#.. => .
#.#.. => .
...#. => .
.#... => #
..... => .
#.... => .
#...# => #
###.# => .
..### => #
###.. => .
##.## => .
##.#. => #
..#.# => #
.###. => .
.#.#. => .
.##.. => #
.#### => .
##... => .
##### => .
..##. => .
#.##. => .
.#..# => #
##..# => .
#.#.# => #
#.### => .
....# => .
#..#. => #
#..## => .
####. => #
.##.# => #"""

def go():
    LEFT_BUF = 60
    rules = [(r[:5], r[-1]) for r in rules_str.splitlines()]
    state = "####..##.##..##..#..###..#....#.######..###########.#...#.##..####.###.#.###.###..#.####..#.#..##..#"
    state = ("."*LEFT_BUF) + state + ("."*60)

    print 0, state

    for i in range(1, 3000):
        successor = ["."] * len(state)

        for rule, result in rules:
            start = 0

            while start + 2 < len(state):
                loc = state.find(rule, start)
                if loc == -1:
                    break

                successor[loc + 2] = result
                start = loc + 1

        state = ''.join(successor)
        print i, state

    total = 0
    for i, c in enumerate(state, start=-LEFT_BUF):
        if c == "#":
            total += i
    print total


if __name__ == "__main__":
    go()
