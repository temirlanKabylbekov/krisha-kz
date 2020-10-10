import math
from functools import reduce
from operator import getitem


def part_range(part, total, items):
    step = math.ceil(len(items) / total) + 1

    for idx, start in enumerate(range(0, len(items), step)):
        if idx == part:
            return items[start: start + step]


def get_nested_item(data, keys):
    return reduce(getitem, keys, data)
