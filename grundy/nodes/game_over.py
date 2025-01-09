import math

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple, Callable

from ..core.node import Node
from ..core.events import EventType
from ..utils.colors import rgb_to_hex, ColorValue


@dataclass
class AnimationConfig:
    """
    Configuration for animation properties.
    """
    FLASH_SPEED: float = 2 * math.pi
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)

@dataclass
class TextStyle:
    """
    Dataclass to store text rendering properties.
    """
    font_family: str = "Arial"
    game_over_size: int = 48
    winner_size: int = 24
    replay_size: int = 16
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
    A node that handles the game over screen display and interactions.
    """

    def __init__(self, engine) -> None:
        """
        Initialize the GameOverNode.
        """
        super().__init__(engine)
        self._tag = f"gameover-{id(self)}"

        self._game_over_text_id: Optional[int] = None
        self._winner_text_id: Optional[int] = None
        self._flashing_text_id: Optional[int] = None
        self._onclick_id: Optional[str] = None
        
        self._flashing_time: float = 0.0
        self._style = TextStyle()
        self._anim_config = AnimationConfig()

    def on_activated(self) -> None:
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        self._onclick_id = self.engine.viewport.bind("<Button-1>", self._on_click)
        self._setup_display()

    def on_deactivated(self) -> None:
        self.engine.canvas.delete(self._tag)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        if self._onclick_id:
            self.engine.viewport.unbind("<Button-1>", self._onclick_id)

    def _setup_display(self) -> None:
        """
        Initialize all display elements.
        """
        self._draw_game_over_text()
        self._draw_winner_text()
        self._draw_flashing_text()

    def _get_screen_center(self) -> Tuple[float, float]:
        """
        Calculate the screen center coordinates.
        """
        return (
            self.engine.viewport.winfo_width() / 2,
            self.engine.viewport.winfo_height() / 2
        )

    def _draw_game_over_text(self) -> None:
        """
        Render the 'GAME OVER' text.
        """
        center_x, center_y = self._get_screen_center()
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
        center_x, center_y = self._get_screen_center()
        winner_type = WinnerType.PLAYER if self.engine.logic.last_winner == 1 else WinnerType.OPPONENT

        self._winner_text_id = self.engine.canvas.create_text(
            center_x,
            center_y,
            text=f"{winner_type.value} won the game!",
            font=(self._style.font_family, self._style.winner_size),
            fill=self._style.default_color,
            tags=self._tag
        )

    def _draw_flashing_text(self) -> None:
        """
        Render the flashing 'Click to play again' text.
        """
        center_x = self.engine.viewport.winfo_width() / 2
        bottom_y = self.engine.viewport.winfo_height() - 50

        self._flashing_text_id = self.engine.canvas.create_text(
            center_x,
            bottom_y,
            text="Click to play again",
            font=(self._style.font_family, self._style.replay_size),
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

        # Update flashing text position
        if self._flashing_text_id:
            self.engine.canvas.coords(
                self._flashing_text_id,
                center_x,
                height - 50
            )

    def _on_update(self, current_time: float, delta_time: float) -> None:
        """
        Update the flashing text animation.
        """
        if self._flashing_text_id:
            self._flashing_time += delta_time
            color = self._calculate_flash_color(self._flashing_time)
            self.engine.canvas.itemconfig(self._flashing_text_id, fill=color)

    def _calculate_flash_color(self, time: float) -> str:
        """
        Calculate the color for the flashing text effect.
        """
        factor = (1 + math.sin(time * self._anim_config.FLASH_SPEED)) / 2

        r = int(self._anim_config.WHITE[0] * (1 - factor) + self._anim_config.BLACK[0] * factor)
        g = int(self._anim_config.WHITE[1] * (1 - factor) + self._anim_config.BLACK[1] * factor)
        b = int(self._anim_config.WHITE[2] * (1 - factor) + self._anim_config.BLACK[2] * factor)

        return rgb_to_hex((r, g, b))

    def _on_click(self, event) -> None:
        """
        Handle click events to restart the game.
        """
        self.engine.logic.reset()
        self.engine.scenes.switch_to("play")
