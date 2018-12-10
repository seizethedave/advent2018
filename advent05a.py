from itertools import chain

def go():
    with open("advent05.txt", "r") as f:
        s = f.read().rstrip()

    polymer = []

    for c in s:
        polymer.append(c)

        while len(polymer) >= 2 and abs(ord(polymer[-1]) - ord(polymer[-2])) == 32:
            polymer.pop()
            polymer.pop()

    print len(polymer)

if __name__ == "__main__":
    go()
