import math

from dataclasses import dataclass


@dataclass
class Point:
    """
    Represents a 2D point.
    """
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        """
        Calculate Euclidean distance to another point.
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass
class Bounds:
    """
    Represents a rectangular boundary defined by two opposite corners.
    """
    x1: int
    y1: int
    x2: int
    y2: int