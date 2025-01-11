import math

from dataclasses import dataclass
from typing import Tuple, Optional

from ..core.node import Node
from ..core.events import EventType
from ..utils.colors import rgb_to_hex, ColorValue


@dataclass
class TextStyle:
    """
    Dataclass to store text rendering properties.
    """
    font_family: str = "Arial"
    replay_size: int = 16
    default_color: str = "white"


@dataclass
class AnimationConfig:
    """
    Configuration for animation properties.
    """
    FLASH_SPEED: float = 2 * math.pi
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)


class ClickPlayNode(Node):
    """
    A node that handles "Click to play" interaction.
    """

    def __init__(self, engine) -> None:
        """
        Initializes the ClickPlay node.
        """
        super().__init__(engine)
        self._tag = f"clickplay-{id(self)}"

        self._flashing_text_id: Optional[int] = None
        self._onclick_id: Optional[str] = None

        self._flashing_time: float = 0.0
        self._anim_config = AnimationConfig()
        self._style = TextStyle()

    def on_activated(self) -> None:
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        self._onclick_id = self.engine.viewport.bind("<Button-1>", self._on_click)
        self._draw_flashing_text()

    def on_deactivated(self) -> None:
        self.engine.canvas.delete(self._tag)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        if self._onclick_id:
            self.engine.viewport.unbind("<Button-1>", self._onclick_id)

    def _draw_flashing_text(self) -> None:
        """
        Render the flashing 'Click to play again' text.
        """
        width, height = self.engine.viewport.get_size()

        center_x = width / 2
        bottom_y = height - 50

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
