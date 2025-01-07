from ..core.events import EventType
from ..core.node import Node

PADDING_BOTTOM = 20
PADDING_LEFT = 20


class MoveHistoryNode(Node):
    def __init__(self, engine):
        super().__init__(engine)

        self._text_item = None
        self._move_history = []

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
            PADDING_LEFT,
            height - PADDING_BOTTOM,
            text="No move has been played yet.",
            fill="white",
            font=("Arial", 16),
            anchor="sw"
        )

    def _on_move_made(self, author, old_pile, new_pile1, new_pile2):
        author_name = "Player" if author == 1 else "Computer"
        move_text = f"{author_name}: {old_pile.size} → {new_pile1.size}, {new_pile2.size}"
        self._move_history.append(move_text)

        if len(self._move_history) > 3:
            self._move_history.pop(0)

        self.engine.canvas.itemconfig(self._text_item, text="\n".join(self._move_history))

    def _on_resize(self, width, height):
        # Update text position on resize
        self.engine.canvas.coords(self._text_item, PADDING_LEFT, height - PADDING_BOTTOM)
