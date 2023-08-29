import math
from typing import Tuple, List

import numpy


def number_of_digits(n: int) -> int:
    if n > 0:
        digits = int(math.log10(n)) + 1
    elif n == 0:
        digits = 1
    else:
        digits = int(math.log10(-n)) + 2  # +1 if you don't count the '-'
    return digits


def tiles_in_circle(center_x: float, center_y: float, radius: float) -> List[Tuple[int, int]]:
    top = math.ceil(center_y - radius)
    bottom = math.floor(center_y + radius)
    left = math.ceil(center_x - radius)
    right = math.floor(center_x + radius)
    tile_list: List[Tuple[int, int]] = []
    for y in range(top, bottom):
        for x in range(left, right):
            if inside_circle(center_x, center_y, x, y, radius):
                tile_list.append((x, y))
    print(tile_list)
    return tile_list


def inside_circle(center_x: float, center_y: float, tile_x: float, tile_y: float, radius: float) -> bool:
    dx = center_x - tile_x
    dy = center_y - tile_y
    distance_squared = dx * dx + dy * dy
    return distance_squared <= radius * radius
