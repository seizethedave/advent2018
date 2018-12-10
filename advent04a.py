from collections import Counter
from datetime import datetime
import re

def find_numbers(s):
    return re.findall(r'\d+', s)

class Guard(object):
    def __init__(self, id):
        self.id = id
        self.sleep_counts = Counter()
        self.sleep_start = None

    def wake(self, time):
        self.sleep_counts.update(range(self.sleep_start, time.minute))
        self.sleep_start = None

    def sleep(self, time):
        self.sleep_start = time.minute

    @property
    def total_minutes_asleep(self):
        return sum(self.sleep_counts.itervalues())

    @property
    def sleepiest_minute(self):
        if not self.sleep_counts:
            return -1

        return self.sleep_counts.most_common(1)[0][0]

    def __repr__(self):
        return "<Guard {}>".format(self.id)

def go():
    with open("advent04.txt", "r") as f:
        lines = f.read().splitlines()

    lines.sort()

    guards = {}
    guard = None

    for line in lines:
        line = line.lstrip("[")
        date_str = line[:16]
        date = datetime(*map(int, find_numbers(date_str)))
        line = line[18:]

        if line.startswith("Guard"):
            guard_num = int(find_numbers(line)[0])

            try:
                guard = guards[guard_num]
            except KeyError:
                guard = guards[guard_num] = Guard(guard_num)
        elif line == "falls asleep":
            assert guard is not None
            guard.sleep(date)
        elif line == "wakes up":
            assert guard is not None
            guard.wake(date)

    best = max(guards.itervalues(), key=lambda g: g.total_minutes_asleep)
    print best.id * best.sleepiest_minute


if __name__ == "__main__":
    go()
