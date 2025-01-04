import numpy as np

from typing import List, Optional

from ..core.events import EventType
from ..core.node import Node
from ..utils import rgb_to_hex

PARTICLE_SPEED = 16
MIN_SPEED = 0.3
MAX_SPEED = 1.5
MIN_RADIUS = 0.5
MAX_RADIUS = 1
INTENSITY_THRESHOLD = 0.12


class ParticlesNode(Node):
    def __init__(
        self,
        engine,
        density: float = 0.0001,  # particles per pixel
    ):
        super().__init__(engine)
        self._tag = f"id-{id(self)}"
        self._density = density

        # Particle state array [x, y, speed, radius, intensity]
        self._particles: Optional[np.ndarray] = None
        self._ovals: List[int] = []  # Store canvas oval IDs

    def _initialize_particles(self) -> None:
        """
        Initialize or reinitialize the particle system
        """
        width, height = self.engine.viewport.get_size()
        num_particles = int(self._density * width * height)

        # Create particle state array
        self._particles = np.zeros((num_particles, 5), dtype=np.float32)

        # Initialize random positions
        self._particles[:, 0] = np.random.uniform(0, width, num_particles)  # x
        self._particles[:, 1] = np.random.uniform(0, height, num_particles)  # y
        self._particles[:, 2] = np.random.uniform(MIN_SPEED, MAX_SPEED, num_particles)  # speed
        self._particles[:, 3] = np.random.uniform(MIN_RADIUS, MAX_RADIUS, num_particles)  # radius
        self._particles[:, 4] = 0  # intensity

        # Create canvas ovals for each particle
        self._ovals = []
        for _ in range(num_particles):
            oval_id = self.engine.canvas.create_oval(
                0, 0, 0, 0,
                fill="",
                outline="",
                state="hidden",
                tags=self._tag
            )
            self._ovals.append(oval_id)

    def on_activated(self) -> None:
        """
        Handle node activation
        """
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)

        self._initialize_particles()

    def on_deactivated(self) -> None:
        """
        Handle node deactivation
        """
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)

        self.engine.canvas.delete(self._tag)
        self._ovals = []
        self._particles = None

    def _on_update(self, ct: float, dt: float) -> None:
        """
        Update particle positions and intensities
        """
        if self._particles is None:
            return

        # Update positions
        speed_dt = self._particles[:, 2] * PARTICLE_SPEED * dt
        self._particles[:, 1] += speed_dt

        # Reset particles that go off screen
        width, height = self.engine.viewport.get_size()
        off_screen = self._particles[:, 1] > height
        if np.any(off_screen):
            self._particles[off_screen, 1] = 0
            self._particles[off_screen, 0] = np.random.uniform(0, width, off_screen.sum())

        # Update intensities using sine wave
        self._particles[:, 4] = 0.5 + 0.5 * np.sin((ct % (2 * np.pi)) + self._particles[:, 0])

        self._render()

    def _render(self) -> None:
        """
        Render all particles
        """
        if self._particles is None:
            return

        canvas = self.engine.canvas
        for i, (x, y, _, radius, intensity) in enumerate(self._particles):
            if intensity < INTENSITY_THRESHOLD:
                canvas.itemconfig(self._ovals[i], state="hidden")
                continue

            # Calculate oval coordinates
            x1, y1 = x - radius, y - radius
            x2, y2 = x + radius, y + radius

            scaled_intensity = int(intensity * 255)
            color = rgb_to_hex((scaled_intensity, scaled_intensity, scaled_intensity))

            # Update oval position and appearance
            canvas.coords(self._ovals[i], x1, y1, x2, y2)
            canvas.itemconfig(
                self._ovals[i],
                state="normal",
                fill=color
            )

    def _on_resize(self, _width: int, _height: int) -> None:
        """
        Handle window resize events
        """
        self._initialize_particles()