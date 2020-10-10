import logging
import math
from functools import reduce
from operator import getitem


def part_range(part, total, items):
    step = math.ceil(len(items) / total) + 1

    for idx, start in enumerate(range(0, len(items), step)):
        if idx == part:
            return items[start: start + step]


def get_nested_item(data, keys):
    try:
        return reduce(getitem, keys, data)
    except Exception as e:
        logging.error(f'{e} for data: {data} and keys: {keys} in get_nested_item')
        return None
