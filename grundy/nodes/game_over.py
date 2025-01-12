from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Callable

from grundy.core.node import Node
from grundy.core.events import EventType


@dataclass
class TextStyle:
    """
    Dataclass to store text rendering properties.
    """
    font_family: str = "Arial"
    game_over_size: int = 48
    winner_size: int = 24
    game_over_color: str = "red"
    default_color: str = "white"

class WinnerType(Enum):
    """
    Enum to represent different winner types.
    """
    PLAYER = "You"
    OPPONENT = "He"

class GameOverNode(Node):
    """
    A node that handles the game over screen display.
    """

    def __init__(self, engine) -> None:
        """
        Initialize the GameOver node.
        """
        super().__init__(engine)
        self._tag = f"gameover-{id(self)}"

        self._game_over_text_id: Optional[int] = None
        self._winner_text_id: Optional[int] = None
        
        self._style = TextStyle()

    def on_activated(self) -> None:
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        self._setup_display()

    def on_deactivated(self) -> None:
        self.engine.canvas.delete(self._tag)
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_window_update)

    def _setup_display(self) -> None:
        """
        Initialize all display elements.
        """
        self._draw_game_over_text()
        self._draw_winner_text()

    def _draw_game_over_text(self) -> None:
        """
        Render the 'GAME OVER' text.
        """
        center_x, center_y = self.engine.viewport.get_center()
        self._game_over_text_id = self.engine.canvas.create_text(
            center_x,
            center_y - 50,
            text="GAME OVER",
            font=(self._style.font_family, self._style.game_over_size, "bold"),
            fill=self._style.game_over_color,
            tags=self._tag
        )

    def _draw_winner_text(self) -> None:
        """
        Render the winner announcement text.
        """
        center_x, center_y = self.engine.viewport.get_center()
        winner_type = WinnerType.PLAYER if self.engine.logic.last_winner == 1 else WinnerType.OPPONENT

        self._winner_text_id = self.engine.canvas.create_text(
            center_x,
            center_y,
            text=f"{winner_type.value} won the game!",
            font=(self._style.font_family, self._style.winner_size),
            fill=self._style.default_color,
            tags=self._tag
        )

    def _on_window_update(self, width: float, height: float) -> None:
        """
        Handle window resize events by updating text positions.
        """
        center_x = width // 2
        center_y = height // 2

        # Update game over text position
        if self._game_over_text_id:
            self.engine.canvas.coords(
                self._game_over_text_id,
                center_x,
                center_y - 50
            )

        # Update winner text position
        if self._winner_text_id:
            self.engine.canvas.coords(
                self._winner_text_id,
                center_x,
                center_y
            )