import math

from dataclasses import dataclass
from typing import Tuple, Optional, Literal

from grundy.core.node import Node
from grundy.core.events import EventType
from grundy.utils.colors import rgb_to_hex, lerp_color


@dataclass
class TextStyle:
    """
    Dataclass to store text rendering properties.
    """
    font_family: str = "Arial"
    font_size: int = 16
    default_color: str = "white"
    padding: int = 50


@dataclass
class AnimationConfig:
    """
    Configuration for animation properties.
    """
    flash_speed: float = 2 * math.pi
    color_from: Tuple[int, int, int] = (255, 255, 255)
    color_to: Tuple[int, int, int] = (0, 0, 0)


class FlashingTextNode(Node):
    """
    A node that handles "Click to play" interaction.
    """

    def __init__(self, engine, text: str, anchor: Literal["bottom", "top"] = "bottom") -> None:
        """
        Initializes the ClickPlay node.
        """
        super().__init__(engine)
        self._tag = f"flashingtext-{id(self)}"

        self._text = text
        self._anchor = anchor
        self._anim_config = AnimationConfig()
        self._style = TextStyle()

        self._flashing_text_id: int = 0
        self._flashing_time: float = 0.0

    def on_activated(self) -> None:
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_window_update)
        self._create_text()

    def on_deactivated(self) -> None:
        self.engine.canvas.delete(self._tag)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_window_update)

    def _create_text(self) -> None:
        """
        Render the flashing text.
        """
        width, height = self.engine.viewport.get_size()
        center_x, bottom_y = width / 2, height - 50
        y = self._style.padding if self._anchor == "top" else height - self._style.padding

        self._flashing_text_id = self.engine.canvas.create_text(
            center_x,
            y,
            text=self._text,
            font=(self._style.font_family, self._style.font_size),
            fill=self._style.default_color,
            tags=self._tag
        )

    def _on_window_update(self, width: float, height: float) -> None:
        """
        Handle window resize events by updating text positions.
        """
        center_x = width // 2
        y = self._style.padding if self._anchor == "top" else height - self._style.padding

        self.engine.canvas.coords(
            self._flashing_text_id,
            center_x,
            y
        )

    def _on_update(self, current_time: float, delta_time: float) -> None:
        """
        Update the flashing text animation.
        """
        self._flashing_time += delta_time
        color = self._calculate_flash_color(self._flashing_time)
        self.engine.canvas.itemconfig(self._flashing_text_id, fill=color)

    def _calculate_flash_color(self, time: float) -> str:
        """
        Calculate the color for the flashing text effect using linear interpolation.
        """
        factor = (1 + math.sin(time * self._anim_config.flash_speed)) / 2

        interpolated_color = lerp_color(
            self._anim_config.color_from,
            self._anim_config.color_to,
            factor
		)
        return rgb_to_hex(interpolated_color)
