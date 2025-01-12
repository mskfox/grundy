import math

from dataclasses import dataclass
from typing import List

from grundy.nodes.atoms.utils import ELECTRON_RADIUS, ELECTRON_SPEED_FACTOR


@dataclass
class OrbitConfig:
    """
    Configuration for orbit visualization.
    """
    orbit_color: str = "black"
    electron_fill: str = "red"
    electron_outline: str = "black"


class Orbit:
    """
    Represents an electron orbit around an atomic nucleus.
    """

    def __init__(
        self,
        engine,
        nucleus_x: int,
        nucleus_y: int,
        radius: int,
        electrons: int,
        config: OrbitConfig = OrbitConfig()
    ):
        """
        Initialize an electron orbit.

        Args:
            engine: The rendering engine
            nucleus_x: X-coordinate of the nucleus center
            nucleus_y: Y-coordinate of the nucleus center
            radius: Orbit radius
            electrons: Number of electrons in this orbit
            config: Visualization configuration
        """
        self.engine = engine
        self._tag = f"orbit-{id(self)}"
        self.config = config

        self.nucleus_x = nucleus_x
        self.nucleus_y = nucleus_y
        self.radius: int = radius
        self.size: int = electrons

        self._electrons: List[int] = []

    def update(self, current_time: float, delta_time: float) -> None:
        """
        Update electron positions in the orbit.

        Args:
            current_time: Current simulation time
            delta_time: Time elapsed since last update
        """
        canvas = self.engine.canvas
        # Speed factor is inversely proportional to the orbit radius. It
        # decreases as the radius increase.
        speed_factor = ELECTRON_SPEED_FACTOR / self.radius

        for i, electron_id in enumerate(self._electrons):
            spatial_offset = i / self.size
            temporal_offset = current_time * speed_factor
            normalized_angle = spatial_offset + temporal_offset

            angle = 2 * math.pi * normalized_angle
            
            x = self.nucleus_x + self.radius * math.cos(angle)
            y = self.nucleus_y + self.radius * math.sin(angle)

            bounds = self._calculate_electron_bounds(x, y)
            canvas.coords(electron_id, *bounds)

    def draw(self) -> None:
        """
        Draw the orbit path and its electrons.
        """
        self._draw_orbit_path()
        self._draw_electrons()

    def clear(self) -> None:
        """
        Remove all visual elements of the orbit.
        """
        self.engine.canvas.delete(self._tag)

    def _draw_orbit_path(self) -> None:
        """
        Draw the circular path of the orbit.
        """
        self.engine.canvas.create_circle(
            self.nucleus_x,
            self.nucleus_y,
            self.radius,
            outline=self.config.orbit_color,
            tags=self._tag
        )

    def _draw_electrons(self) -> None:
        """
        Create and position electrons on the orbit.
        """
        canvas = self.engine.canvas

        for i in range(self.size):
            angle = 2 * math.pi * i / self.size
            x = self.nucleus_x + self.radius * math.cos(angle)
            y = self.nucleus_y + self.radius * math.sin(angle)

            electron_id = canvas.create_circle(
                x,
                y,
                ELECTRON_RADIUS,
                fill=self.config.electron_fill,
                outline=self.config.electron_outline,
                tags=self._tag
            )
            self._electrons.append(electron_id)

    @staticmethod
    def _calculate_electron_bounds(x: float, y: float) -> tuple[float, float, float, float]:
        """
        Calculate the bounding box for an electron at given coordinates.

        Args:
            x: Center x-coordinate
            y: Center y-coordinate

        Returns:
            Tuple of (left, top, right, bottom) coordinates
        """
        return (
            x - ELECTRON_RADIUS,
            y - ELECTRON_RADIUS,
            x + ELECTRON_RADIUS,
            y + ELECTRON_RADIUS
        )