from grundy.core.node import Node


class CoolingTowerNode(Node):
    def __init__(self, engine, x):
        super().__init__(engine)
        self._tag = f"coolingtower-{id(self)}"

        _, viewport_height = self.engine.viewport.get_size()
        self._x, self._y = x, viewport_height
        self._width, self._height = 120, 180

    def on_activated(self) -> None:
        """
        Handle node activation
        """
        self._create_cooling_tower()

    def on_deactivated(self) -> None:
        """
        Handle node deactivation
        """
        canvas = self.engine.canvas
        canvas.delete(self._tag)

    def _create_cooling_tower(self) -> None:
        canvas = self.engine.canvas
        w, h = self._width, self._height

        relative_offsets = [
            (-w // 2, 0),           # Bottom-left
            (w // 2, 0),            # Bottom-right
            (w // 3, -h // 2),      # Mid-top-right (neck)
            (w // 4, -h),           # Top-right (flared top)
            (-w // 4, -h),          # Top-left (flared top)
            (-w // 3, -h // 2)      # Mid-top-left (neck)
        ]
        points = [(self._x + dx, self._y + dy) for dx, dy in relative_offsets]

        canvas.create_polygon(
            points,
            fill="lightgrey",
            outline="black",
            tags=self._tag
        )