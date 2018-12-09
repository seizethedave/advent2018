from collections import deque
from itertools import cycle, islice

PLAYERS = 432
LAST_MARBLE = 71019 * 100

def go():
    scores = [0] * PLAYERS
    marbles = deque([0])
    max_score = 0

    for marble, player in enumerate(islice(cycle(xrange(PLAYERS)), LAST_MARBLE + 1), start=1):
        if (marble % 23) == 0:
            marbles.rotate(7)
            play_score = marble + marbles.popleft()
        else:
            # Regular.
            marbles.rotate(-2)
            marbles.appendleft(marble)
            play_score = 0

        scores[player] += play_score
        max_score = max(max_score, scores[player])

    print max_score

if __name__ == "__main__":
    go()
