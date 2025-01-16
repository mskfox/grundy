from dataclasses import dataclass

from grundy.core.events import EventType
from grundy.core.node import Node


@dataclass
class NodeConfig:
    """
    Configuration for the MoveHistory node.
    """
    padding_bottom: int = 20
    padding_left: int = 20
    max_history_capacity: int = 3


class MoveHistoryNode(Node):
    """
    Node which tracks and displays the move history.

    This node updates the canvas with the history of moves made by the players,
    displays them in a text format, and ensures the display remains up-to-date
    with every move and window resize event.
    """
    def __init__(self, engine):
        """
        Initialize the move history node.
        """
        super().__init__(engine)
        self.config = NodeConfig()

        self._text_item = None
        self._move_history = []

    def on_activated(self) -> None:
        """
        Handle node activation
        """
        self._move_history = []

        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.subscribe(EventType.MOVE_MADE, self._on_move_made)
        self._create_text()

    def on_deactivated(self) -> None:
        """
        Handle node deactivation
        """
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.unsubscribe(EventType.MOVE_MADE, self._on_move_made)
        self.engine.canvas.delete(self._text_item)

    def _create_text(self):
        """
        Render the text item.
        """
        canvas = self.engine.canvas
        width, height = self.engine.viewport.get_size()
        self._text_item = canvas.create_text(
            self.config.padding_left,
            height - self.config.padding_bottom,
            text="No move has been played yet.",
            fill="white",
            font=("Arial", 16),
            anchor="sw"
        )

    def _on_move_made(self, author, old_pile, new_pile1, new_pile2):
        """
        Updates the move history and modifies the displayed text with the latest move.
        """
        author_name = "You" if author == 1 else "Him"
        move_text = f"{author_name}: {old_pile.size} → {new_pile1.size}, {new_pile2.size}"
        self._move_history.append(move_text)

        if len(self._move_history) > self.config.max_history_capacity:
            self._move_history.pop(0)

        self.engine.canvas.itemconfig(self._text_item, text="\n".join(self._move_history))

    def _on_resize(self, _, height):
        """
        Adjusts the position when the window is resized.
        """
        cfg = self.config
        self.engine.canvas.coords(self._text_item, cfg.padding_left, height - cfg.padding_bottom)
