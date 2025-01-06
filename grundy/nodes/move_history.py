from ..core.events import EventType
from ..core.node import Node

PADDING_BOTTOM = 20


class MoveHistoryNode(Node):
    def __init__(
        self,
        engine
    ):
        super().__init__(engine)

        self._text_item = None

    def on_activated(self) -> None:
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.subscribe(EventType.MOVE_MADE, self._on_move_made)
        self._draw_text()

    def on_deactivated(self) -> None:
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.unsubscribe(EventType.MOVE_MADE, self._on_move_made)
        self.engine.canvas.delete(self._text_item)

    def _draw_text(self):
        canvas = self.engine.canvas
        width, height = self.engine.viewport.get_size()
        self._text_item = canvas.create_text(
            width // 2,
            height - PADDING_BOTTOM,
            text="No move has been played yet.",
            fill="white",
            font=("Arial", 16),
            anchor="s"
        )

    def _on_move_made(self, old_size, new_size1, new_size2):
        self.engine.canvas.itemconfig(self._text_item, text=f"Atom of size {old_size} got splitted into atoms of size {new_size1} and {new_size2}")

    def _on_resize(self, width, height):
        self.engine.canvas.coords(self._text_item, width // 2, height - PADDING_BOTTOM)