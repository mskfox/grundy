import math

from typing import List

from .utils import ELECTRON_RADIUS


class Orbit:
    def __init__(self, engine, nucleus_x: int, nucleus_y: int, radius: int, electrons: int):
        self.engine = engine
        self._tag = f"id-{id(self)}"

        self.nucleus_x = nucleus_x
        self.nucleus_y = nucleus_y
        self.radius: int = radius
        self.size: int = electrons

        self._electrons: List[int] = []

    def update(self, ct: float, dt: float):
        canvas = self.engine.canvas
        for i, electron_id in enumerate(self._electrons):
            speed_factor = 1 / self.radius * 20
            angle = 2 * math.pi * i / self.size + ct * speed_factor

            x = self.nucleus_x + self.radius * math.cos(angle)
            y = self.nucleus_y + self.radius * math.sin(angle)

            electron_bounds = (x - ELECTRON_RADIUS, y - ELECTRON_RADIUS, x + ELECTRON_RADIUS, y + ELECTRON_RADIUS)
            canvas.coords(electron_id, *electron_bounds)

    def draw(self):
        self._draw_orbit()
        self._draw_electrons()

    def clear(self):
        self.engine.canvas.delete(self._tag)

    def _draw_orbit(self):
        canvas = self.engine.canvas
        canvas.create_circle(
            self.nucleus_x, self.nucleus_y, self.radius,
            outline="black",
            tags=self._tag
        )

    def _draw_electrons(self):
        canvas = self.engine.canvas
        for i in range(self.size):
            angle = 2 * math.pi * i / self.size
            x = self.nucleus_x + self.radius * math.cos(angle)
            y = self.nucleus_y + self.radius * math.sin(angle)

            electron_id = canvas.create_circle(
                x, y, ELECTRON_RADIUS,
                fill="red",
                outline="black",
                tags=self._tag
            )
            self._electrons.append(electron_id)