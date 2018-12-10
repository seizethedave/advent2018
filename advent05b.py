def react_polymer(s):
    polymer = []

    for c in s:
        polymer.append(c)

        while len(polymer) >= 2 and abs(ord(polymer[-1]) - ord(polymer[-2])) == 32:
            polymer.pop()
            polymer.pop()

    return polymer

def go():
    with open("advent05.txt", "r") as f:
        s = f.read().rstrip()

    kinds = set(c.lower() for c in s)

    polymers = (
        react_polymer(c for c in s if c.lower() != kind)
        for kind in kinds
    )

    print min(len(p) for p in polymers)

if __name__ == "__main__":
    go()
