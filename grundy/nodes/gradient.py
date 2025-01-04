from typing import Tuple

from ..core.events import EventType
from ..core.node import Node
from ..utils.colors import ColorValue


class GradientNode(Node):
    def __init__(
            self,
            engine,
            start_color: ColorValue = "#000000",
            end_color: ColorValue = "#FFFFFF",
            direction: str = "vertical"
    ):
        super().__init__(engine)
        self._tag = f"id-{id(self)}"

        self._start_color: ColorValue = start_color
        self._end_color: ColorValue = end_color
        self._direction: str = direction

    def on_activated(self) -> None:
        """
        Subscribe to window resize events when active
        """
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self._draw_gradient(self.engine.viewport.get_size())

    def on_deactivated(self) -> None:
        """
        Unsubscribe from window resize events when inactive
        """
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.canvas.delete(self._tag)

    def _on_resize(self, width: int, height: int) -> None:
        """
        Handle window resize events
        """
        self._draw_gradient((width, height))

    def _draw_gradient(self, bottom_right: Tuple[int, int]) -> None:
        """
        Draw or redraw the gradient
        """
        self.engine.canvas.delete(self._tag)
        self.engine.canvas.create_gradient(
            self._start_color,
            self._end_color,
            (0, 0),
            bottom_right,
            direction=self._direction,
            tag=self._tag
        )