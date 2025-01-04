import math
import random

from typing import List

NUCLEUS_RADIUS = 10
ELECTRON_RADIUS = 2
ORBIT_DEFAULT_RADIUS = 20
ORBIT_RADIUS_INCREMENT = 10
ATOM_MIN_DISTANCE = 0


def calculate_real_radius(layers: int):
    return NUCLEUS_RADIUS + ORBIT_DEFAULT_RADIUS + layers * ORBIT_RADIUS_INCREMENT


def atoms_overlap(atom1, x, y, radius):
    x1, y1 = atom1.x, atom1.y
    x2, y2 = x, y
    min_distance = calculate_real_radius(len(atom1.layers)) + radius + ATOM_MIN_DISTANCE
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return distance < min_distance


def place_single_atom(x1, y1, x2, y2, existing_atoms, max_attempts=300):
    """
    Try to place a single atom within the rectangle defined by (x1, y1) as the top-left
    and (x2, y2) as the bottom-right corners, avoiding overlap with existing atoms.

    Returns the (x, y) position of the atom if successful, or None if placement fails.
    """
    attempts = 0

    while attempts < max_attempts:
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)

        overlap = False
        for atom in existing_atoms:
            # FIXME: fix real radius
            if atoms_overlap(atom, x, y, calculate_real_radius(1)):
                overlap = True
                break

        if not overlap:
            return x, y

        attempts += 1

    print("Failed to find a position for an atom.")
    return None, None


def electrons_per_orbit(total_electrons: int) -> List[int]:
    orbits = []
    n = 1

    while total_electrons > 0:
        max_electrons = 2 * n ** 2
        current_electrons = min(total_electrons, max_electrons)
        orbits.append(current_electrons)

        total_electrons -= current_electrons
        n += 1

    return orbits