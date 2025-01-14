from dataclasses import dataclass
from typing import Tuple, List, Optional
from grundy.core.node import Node


@dataclass
class PowerPlantConfig:
    """
    Configuration settings for the power plant visualization.
    """
    # Building dimensions
    main_building_width: int = 350
    main_building_height: int = 200
    main_building_bottom_left_offset: int = 60
    utility_building_width: int = 175
    utility_building_height: int = 90

    # Chimney configuration
    num_chimneys: int = 3
    chimney_spacing: int = 115
    chimney_width: int = 55
    chimney_height: int = 180
    chimney_top_width: int = 30

    # Window configuration
    window_rows: int = 3
    window_columns: int = 5
    window_width: int = 40
    window_height: int = 30
    window_margin_x: int = 20
    window_margin_y: int = 30

    # Colors
    main_fill: str = "lightgrey"
    main_outline: str = "black"
    window_fill: str = "lightblue"
    window_outline: str = "darkgrey"
    chimney_fill: str = "lightgrey"
    chimney_outline: str = "black"
    utility_fill: str = "lightgrey"
    utility_outline: str = "black"

    # Layout
    utility_building_offset: int = 40

    # Ventilation configuration
    vent_rows: int = 3
    vent_columns: int = 3
    vent_offset: int = 20
    vent_spacing_x: int = 50
    vent_spacing_y: int = 20
    vent_line_width: int = 2
    vent_line_length: int = 30


class PowerPlantNode(Node):
    """
    A node representing a power plant visualization.
    """

    def __init__(
        self,
        engine,
        x: int,
        config: Optional[PowerPlantConfig] = None
    ):
        """
        Initialize the power plant node.

        Args:
            engine: The rendering engine
            position: (x, y) coordinates for the plant position
            config: Optional custom configuration for the power plant
        """
        super().__init__(engine)
        self._tag = f"powerplant-{id(self)}"

        _, canvas_height = self.engine.viewport.get_size()
        self._x, self._y = x, canvas_height
        self._config = config or PowerPlantConfig()

    def on_activated(self) -> None:
        """
        Handle node activation by creating the power plant visualization.
        """
        self._create_power_plant()

    def on_deactivated(self) -> None:
        """
        Handle node deactivation by removing the visualization.
        """
        self.engine.canvas.delete(self._tag)

    def _create_power_plant(self) -> None:
        """
        Create all components of the power plant.
        """
        self._create_main_building()
        self._create_windows()
        self._create_chimneys()
        self._create_utility_building()

    def _create_main_building(self) -> None:
        """
        Create the main building structure.
        """
        w, h = self._config.main_building_width, self._config.main_building_height

        relative_offsets = [
            (-w // 2 - self._config.main_building_bottom_left_offset, 0), # Bottom-left
            (w // 2, 0), # Bottom-right
            (w // 2, -h), # Top-right
            (-w // 2, -h) # Top-left
        ]
        points = self._calculate_polygon_points(relative_offsets)

        self.engine.canvas.create_polygon(
            points,
            fill=self._config.main_fill,
            outline=self._config.main_outline,
            tags=self._tag
        )

    def _create_windows(self) -> None:
        """
        Create windows on the main building.
        """
        config = self._config
        building_height = config.main_building_height

        total_window_width = config.window_columns * config.window_width

        start_x = self._x - (total_window_width // 2) - (config.window_width // 2)
        start_y = self._y - building_height + config.window_margin_y

        for row in range(config.window_rows):
            for col in range(config.window_columns):
                x = start_x + (col * (config.window_width + config.window_margin_x))
                y = start_y + (row * (config.window_height + config.window_margin_y))
                self._create_window(x, y)

    def _create_window(self, x: int, y: int) -> None:
        """
        Create a window.
        """
        config = self._config
        self.engine.canvas.create_rectangle(
            x - config.window_width // 2, y - config.window_height // 2,
            x + config.window_width // 2, y + config.window_height // 2,
            fill=config.window_fill,
            outline=config.window_outline,
            tags=self._tag
        )

    def _create_chimneys(self) -> None:
        """
        Create multiple chimneys with configured spacing.
        """
        config = self._config
        chimney_y = self._y - config.main_building_height - config.chimney_height // 2

        for i in range(config.num_chimneys):
            offset = (config.num_chimneys - 1) * config.chimney_spacing // 2
            chimney_x = self._x - offset + (i * config.chimney_spacing)
            self._create_chimney(chimney_x, chimney_y)

    def _create_chimney(self, x: int, y: int) -> None:
        """
        Create a single chimney.
        """
        config = self._config
        self.engine.canvas.create_trapeze(
            x, y,
            config.chimney_width,
            config.chimney_top_width,
            config.chimney_height,
            fill=config.chimney_fill,
            outline=config.chimney_outline,
            tags=self._tag
        )

    def _create_utility_building(self) -> None:
        """
        Create the utility building with ventilation.
        """
        config = self._config
        width, height = config.utility_building_width, config.utility_building_height

        # Calculate position relative to main building
        x = self._x - width - config.utility_building_offset
        y = self._y - height // 2

        self._create_utility_structure(x, y, width, height)
        self._create_ventilation_lines(x, y, width // 2, height // 2)

    def _create_utility_structure(self, x: int, y: int, width: int, height: int) -> None:
        """
        Create the main utility building structure.
        """
        config = self._config
        self.engine.canvas.create_rectangle(
            x - width // 2, y - height // 2,
            x + width // 2, y + height // 2,
            fill=config.utility_fill,
            outline=config.utility_outline,
            tags=self._tag
        )

    def _create_ventilation_lines(
        self,
        x: int, y: int,
        half_width: int, half_height: int
    ) -> None:
        """
        Create ventilation lines pattern.
        """
        config = self._config

        for col in range(config.vent_columns):
            for row in range(config.vent_rows):
                start_x = x - half_width + config.vent_offset + config.vent_spacing_x * col
                start_y = y - half_height + config.vent_offset + config.vent_spacing_y * row

                self.engine.canvas.create_line(
                    start_x, start_y,
                    start_x + config.vent_line_length, start_y,
                    fill=config.utility_outline,
                    width=config.vent_line_width,
                    tags=self._tag
                )

    def _calculate_polygon_points(self, relative_offsets: List[Tuple[int, int]]) -> List[int]:
        """
        Calculate absolute polygon points from relative offsets.
        """
        points = []
        for dx, dy in relative_offsets:
            points.extend([self._x + dx, self._y + dy])
        return points