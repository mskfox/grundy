from typing import List

from ...core.logic import Pile
from .orbit import Orbit
from .utils import electrons_per_orbit, calculate_real_radius, NUCLEUS_RADIUS, ORBIT_DEFAULT_RADIUS, ORBIT_RADIUS_INCREMENT


class Atom:
    def __init__(self, engine, x: int, y: int, pile_id: int, pile_size: int):
        self.engine = engine
        self._tag = f"id-{id(self)}"

        self.x: int = x
        self.y: int = y
        self.size: int = pile_size
        self.pile_id = pile_id
        self.layers = electrons_per_orbit(self.size)

        self._orbits: List[Orbit] = []

    def draw(self):
        self._draw_nucleus()
        self._draw_orbits()

    def clear(self):
        for orbit in self._orbits:
            orbit.clear()
        self.engine.canvas.delete(self._tag)

    def update(self, ct: float, dt: float):
        for orbit in self._orbits:
            orbit.update(ct, dt)

    def _draw_nucleus(self):
        canvas = self.engine.canvas
        canvas.create_gradient_circle(
            self.x, self.y, NUCLEUS_RADIUS,
            start_color="#000000",
            end_color="#FFFFFF",
            steps=10,
            tags=self._tag
        )

    def _draw_orbits(self):
        for i, electrons in enumerate(self.layers):
            radius = ORBIT_DEFAULT_RADIUS + ORBIT_RADIUS_INCREMENT * i # Assuming a distance of 10 between orbits and starting from 20
            orbit = Orbit(self.engine, self.x, self.y, radius, electrons)
            orbit.draw()

            self._orbits.append(orbit)