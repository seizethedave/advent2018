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

def go():
    LIMIT = 10000

    print sum(
        1 if sum(distance(coordinate, pt) for pt in coordinates) < LIMIT else 0
        for coordinate in iter_all_cooordinates()
    )

if __name__ == "__main__":
    go()
