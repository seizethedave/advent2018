from collections import Counter
import heapq
from operator import itemgetter
import sys

coordinates = [
   (181, 47), (337, 53), (331, 40), (137, 57), (200, 96), (351, 180), (157, 332),
   (113, 101), (285, 55), (189, 188), (174, 254), (339, 81), (143, 61), (131, 155),
   (239, 334), (357, 291), (290, 89), (164, 149), (248, 73), (311, 190),
   (54, 217), (285, 268), (354, 113), (318, 191), (182, 230), (156, 252), (114, 232),
   (159, 299), (324, 280), (152, 155), (295, 293), (194, 214), (252, 345),
   (233, 172), (272, 311), (230, 82), (62, 160), (275, 96), (335, 215), (185, 347),
   (134, 272), (58, 113), (112, 155), (220, 83), (153, 244), (279, 149),
   (302, 167), (185, 158), (72, 91), (264, 67)
]

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_frame():
    min_x = min_y = sys.maxint
    max_x = max_y = -sys.maxint - 1

    for x, y in coordinates:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return (min_x, min_y), (max_x, max_y)

def iter_frame_cooordinates():
    """
    xxxxxxxx
    x      x
    x      x
    xxxxxxxx
    """
    (left, top), (right, bottom) = get_frame()

    for x in range(left, right + 1):
        yield x, top

    for y in range(top + 1, bottom):
        yield left, y
        yield right, y

    for x in range(left, right + 1):
        yield x, bottom

def iter_all_cooordinates():
    """
    xxxxxxxx
    xxxxxxxx
    xxxxxxxx
    xxxxxxxx
    """
    (left, top), (right, bottom) = get_frame()

    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            yield x, y

def find_infinite_coordinates():
    # From every spot on the frame:
    # Find the closest coordinate. That coordinate has an infinite field.
    # Yields them.

    for frame_point in iter_frame_cooordinates():
        yield min(coordinates, key=lambda pt: distance(frame_point, pt))

def go():
    infinite_points = set(find_infinite_coordinates())
    winners = Counter()

    for source in iter_all_cooordinates():
        (dist1, p1), (dist2, p2) = heapq.nsmallest(
            2,
            ((distance(source, p), p) for p in coordinates),
            key=itemgetter(0)
        )

        if dist1 < dist2 and p1 not in infinite_points:
            winners[p1] += 1
        else:
            # Equidistant or closest is infinite. Do nothing.
            pass

    print winners.most_common(1)


if __name__ == "__main__":
    go()
