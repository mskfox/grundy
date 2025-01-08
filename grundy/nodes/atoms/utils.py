"""
Utility functions and constants for atom visualization.
"""

import random

from typing import List, Tuple, Optional

from ...utils.geom import Point, Bounds


# Higher values equals to a faster rotation
ELECTRON_SPEED_FACTOR = 6

NUCLEUS_RADIUS = 16
ELECTRON_RADIUS = 2
ORBIT_FIRST_RADIUS_INCREMENT = 10
ORBIT_RADIUS_INCREMENT = 10
ATOM_MIN_DISTANCE = 6


def calculate_real_radius(layers: int) -> float:
    """
    Calculate the total radius of an atom including all electron layers.

    Args:
        layers: Number of electron layers

    Returns:
        Total radius of the atom
    """
    return NUCLEUS_RADIUS + ORBIT_FIRST_RADIUS_INCREMENT + (layers - 1) * ORBIT_RADIUS_INCREMENT


def atoms_overlap(atom1, x: int, y: int, radius: float) -> bool:
    """
    Check if two atoms would overlap at given positions.

    Args:
        atom1: First atom
        x: X-coordinate of second atom
        y: Y-coordinate of second atom
        radius: Radius of second atom

    Returns:
        True if atoms would overlap, False otherwise
    """
    point1 = Point(atom1.x, atom1.y)
    point2 = Point(x, y)
    min_distance = calculate_real_radius(atom1.layers_quantity) + radius + ATOM_MIN_DISTANCE

    return point1.distance_to(point2) < min_distance


def place_single_atom(
        area_bounds: Bounds,
        existing_atoms: List,
        layers_quantity: int,
        max_attempts: int = 300
) -> Tuple[bool, int, int]:
    """
    Try to place a single atom within a rectangular area.

    Args:
        area_bounds: Bundary of the spawning area
        existing_atoms: List of existing atoms to avoid overlap
        max_attempts: Maximum number of placement attempts

    Returns:
        Tuple of (success, x, y) where success is True if placement was successful
    """
    if area_bounds.x2 <= area_bounds.x1 or area_bounds.y2 <= area_bounds.y1:
        return False, 0, 0

    for _ in range(max_attempts):
        x = random.randint(area_bounds.x1, area_bounds.x2)
        y = random.randint(area_bounds.y1, area_bounds.y2)

        if not any(atoms_overlap(atom, x, y, calculate_real_radius(layers_quantity))
                   for atom in existing_atoms):
            return True, x, y

    print("Failed to find a position for an atom.")
    return False, 0, 0


def pick_atom_at(atoms: List, x: int, y: int) -> Optional:
    """
    Find an atom at the given coordinates.

    Args:
        atoms: List of atoms to search
        x: X-coordinate
        y: Y-coordinate

    Returns:
        The atom at the given position or None if not found
    """
    point = Point(x, y)

    for atom in atoms:
        if point.distance_to(Point(atom.x, atom.y)) <= NUCLEUS_RADIUS:
            return atom

    return None


def electrons_per_orbit(total_electrons: int) -> Tuple[int, List[int]]:
    """
    Calculate electron distribution across orbits based on quantum mechanics.

    Args:
        total_electrons: Total number of electrons to distribute

    Returns:
        Amount of layers.
        List of electron counts for each orbit
    """
    orbits = []
    principal_quantum_number = 1

    while total_electrons > 0:
        max_electrons = 2 * principal_quantum_number ** 2
        current_electrons = min(total_electrons, max_electrons)
        orbits.append(current_electrons)

        total_electrons -= current_electrons
        principal_quantum_number += 1

    total_layers = len(orbits)
    return total_layers, orbits