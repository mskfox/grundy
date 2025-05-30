from dataclasses import dataclass
from typing import List

from grundy.core.logic import Pile
from grundy.nodes.atoms.orbit import Orbit
from grundy.nodes.atoms.utils import (
    calculate_electrons_distribution,
    calculate_real_radius,
    NUCLEUS_RADIUS,
    ORBIT_FIRST_RADIUS_INCREMENT,
    ORBIT_RADIUS_INCREMENT,
)


@dataclass
class AtomConfig:
    """
    Configuration for atom visualization.
    """
    nucleus_outer_color: str = "#000000"
    nucleus_inner_color: str = "#B0B0B0"
    nucleus_gradient_steps: int = 10
    font_family: str = "Arial"
    font_size: int = 10
    font_color: str = "red"


class Atom:
    """
    Represents an atom with a nucleus and electron orbits.
    """

    def __init__(
        self,
        engine,
        x: int,
        y: int,
        pile: Pile,
        config: AtomConfig = AtomConfig()
    ):
        """
        Initialize an atom.
        """
        self.engine = engine
        self._tag = f"atom-{id(self)}"
        self.config = config

        self.x: int = x
        self.y: int = y
        self.pile: Pile = pile

        # Calculate electron distribution and dimensions
        self.distribution = calculate_electrons_distribution(self.pile.size)
        self.real_radius = calculate_real_radius(self.distribution.layer_count)

        self._orbits: List[Orbit] = []

    def draw(self) -> None:
        """
        Draw the complete atom with nucleus and orbits.
        """
        self._draw_nucleus()
        self._draw_orbits()

    def clear(self) -> None:
        """
        Remove all visual elements of the atom.
        """
        for orbit in self._orbits:
            orbit.clear()
        self.engine.canvas.delete(self._tag)

    def update(self, current_time: float, delta_time: float) -> None:
        """
        Update the atom's electron positions.

        Args:
            current_time: Current simulation time
            delta_time: Time elapsed since last update
        """
        for orbit in self._orbits:
            orbit.update(current_time, delta_time)

    def _draw_nucleus(self) -> None:
        """
        Draw the atom's nucleus with gradient and size label.
        """
        canvas = self.engine.canvas

        # Draw nucleus with gradient
        canvas.create_gradient_circle(
            self.x,
            self.y,
            NUCLEUS_RADIUS,
            start_color=self.config.nucleus_outer_color,
            end_color=self.config.nucleus_inner_color,
            steps=self.config.nucleus_gradient_steps,
            tags=self._tag
        )

        # Draw size label
        canvas.create_text(
            self.x,
            self.y,
            text=str(self.pile.size),
            font=(
                self.config.font_family,
                self.config.font_size,
                "bold"
            ),
            fill=self.config.font_color,
            tags=self._tag
        )

    def _draw_orbits(self) -> None:
        """
        Create and draw electron orbits.
        """
        for layer_index, electron_count in enumerate(self.distribution.electrons_per_layer):
            radius = NUCLEUS_RADIUS + ORBIT_FIRST_RADIUS_INCREMENT + ORBIT_RADIUS_INCREMENT * layer_index
            orbit = Orbit(
                self.engine,
                self.x,
                self.y,
                radius,
                electron_count,
                self.pile
            )
            orbit.draw()
            self._orbits.append(orbit)