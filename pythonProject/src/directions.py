from enum import Enum


class Directions(Enum):
    RIGHT = (0, 1)
    LEFT = (0, -1)
    DOWN = (1, 0)
    UP = (-1, 0)