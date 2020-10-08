import math


def part_range(part, total, items):
    step = math.ceil(len(items) / total) + 1

    for idx, start in enumerate(range(0, len(items), step)):
        if idx == part:
            return items[start: start + step]
