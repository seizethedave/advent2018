import itertools

def get_lines():
    with open('advent02.txt', 'r') as f:
        for line in f:
            yield line


def off_by_one(id1, id2):
    return 1 == sum(
        1 if x != y else 0 for x, y in zip(id1, id2)
    )

def go():
    lines = list(get_lines())

    for line1, line2 in itertools.combinations(lines, r=2):
        if off_by_one(line1, line2):
            print "".join(a for a, b in zip(line1, line2) if a == b)
            return


if __name__ == "__main__":
    go()
