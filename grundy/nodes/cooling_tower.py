from grundy.core.node import Node


class CoolingTowerNode(Node):
    def __init__(self, engine, x, y):
        super().__init__(engine)
        self._tag = f"coolingtower-{id(self)}"

        self._x, self._y = x, y
        self._width, self._height = 120, 180

    def on_activated(self) -> None:
        self._create_cooling_tower()

    def on_deactivated(self) -> None:
        canvas = self.engine.canvas
        canvas.delete(self._tag)

    def _create_cooling_tower(self) -> None:
        canvas = self.engine.canvas
        x, y = self._x, self._y
        w, h = self._width, self._height

        relative_offsets = [
            (-w // 2, 0),           # Bottom-left
            (w // 2, 0),            # Bottom-right
            (w // 3, -h // 2),      # Mid-top-right (neck)
            (w // 4, -h),           # Top-right (flared top)
            (-w // 4, -h),          # Top-left (flared top)
            (-w // 3, -h // 2)      # Mid-top-left (neck)
        ]
        points = [(x + dx, y + dy) for dx, dy in relative_offsets]

        # Create the polygon representing the cooling tower
        canvas.create_polygon(
            points,
            fill="lightgrey",
            outline="black",
            tags=self._tag
        )