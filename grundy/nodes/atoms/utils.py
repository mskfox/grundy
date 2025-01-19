"""
Utility functions and constants for atom visualization.
"""

import random

from dataclasses import dataclass
from typing import List, Tuple, Optional, TYPE_CHECKING

from grundy.utils.geom import Point, Bounds

if TYPE_CHECKING:
    from grundy.nodes.atoms.atom import Atom


# Higher values equals to a faster rotation
ELECTRON_SPEED_FACTOR = 6

NUCLEUS_RADIUS = 16
ELECTRON_RADIUS = 2.5
ORBIT_FIRST_RADIUS_INCREMENT = 10
ORBIT_RADIUS_INCREMENT = 10
ATOM_MIN_DISTANCE = 6
MAX_PLACEMENT_ATTEMPTS = 300


@dataclass
class ElectronDistribution:
    """
    Result of electron distribution calculation.
    """
    layer_count: int
    electrons_per_layer: List[int]


def calculate_electrons_distribution(total_electrons: int) -> ElectronDistribution:
    """
    Calculate electron distribution across orbits based on quantum mechanics.
    """
    orbits = []
    principal_quantum_number = 1

    while total_electrons > 0:
        max_electrons = 2 * principal_quantum_number ** 2
        current_layer_electrons = min(total_electrons, max_electrons)
        orbits.append(current_layer_electrons)

        total_electrons -= current_layer_electrons
        principal_quantum_number += 1

    return ElectronDistribution(
        layer_count=len(orbits),
        electrons_per_layer=orbits
    )


def calculate_real_radius(layers: int) -> float:
    """
    Calculate the total radius of an atom including all electron layers.
    """
    return NUCLEUS_RADIUS + ORBIT_FIRST_RADIUS_INCREMENT + (layers - 1) * ORBIT_RADIUS_INCREMENT


def atoms_overlap(atom1: 'Atom', x: int, y: int, radius: float) -> bool:
    """
    Check if two atoms would overlap at given positions.
    """
    point1 = Point(atom1.x, atom1.y)
    point2 = Point(x, y)
    min_distance = calculate_real_radius(atom1.distribution.layer_count) + radius + ATOM_MIN_DISTANCE

    return point1.distance_to(point2) < min_distance


def place_single_atom(
    area_bounds: Bounds,
    existing_atoms: List,
    layer_count: int,
) -> Tuple[bool, int, int]:
    """
    Try to place a single atom within a rectangular area.
    Returns a tuple of (success, x, y) where success is True if placement was successful
    """
    if area_bounds.x2 <= area_bounds.x1 or area_bounds.y2 <= area_bounds.y1:
        return False, 0, 0

    for _ in range(MAX_PLACEMENT_ATTEMPTS):
        x = random.randint(area_bounds.x1, area_bounds.x2)
        y = random.randint(area_bounds.y1, area_bounds.y2)

        if not any(
            atoms_overlap(atom, x, y, calculate_real_radius(layer_count))
            for atom in existing_atoms
        ):
            return True, x, y

    return False, 0, 0


def pick_atom_at(atoms: List, x: int, y: int) -> Optional['Atom']:
    """
    Find an atom at the given coordinates.
    """
    point = Point(x, y)

    for atom in atoms:
        if point.distance_to(Point(atom.x, atom.y)) <= NUCLEUS_RADIUS:
            return atom

    return None