from dataclasses import dataclass
from typing import Optional


@dataclass
class WarningConfig:
    """
    Configuration for warning display.
    """
    background_color: str = "#FF0000"
    text_color: str = "#FFFFFF"
    font = ("Arial", 12, "bold")
    padding: int = 12
    message: str = "Failed to place all atoms!"


class AtomWarning:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._tag = f"warning-{id(self)}"
        self._config = WarningConfig()

        self.is_visible = False

        self._text_id: Optional[int] = None
        self._bg_id: Optional[int] = None

    def start_warning(self) -> None:
        """
        Start displaying a warning message.
        """
        if self.is_visible:
            return

        self.is_visible = True

        self._bg_id = self.engine.canvas.create_rectangle(
            0, 0, 0, 0,
            fill=self._config.background_color,
            outline="",
            tags=self._tag,
            width=2
        )

        self._text_id = self.engine.canvas.create_text(
            0, 0,
            text=self._config.message,
            fill=self._config.text_color,
            font=self._config.font,
            tags=self._tag
        )

        self.render()

    def stop_warning(self) -> None:
        """Stop and remove the warning display."""
        if not self.is_visible:
            return

        self.engine.canvas.delete(self._tag)
        self.is_visible = False
        self._text_id = None
        self._bg_id = None

    def render(self) -> None:
        """
        Update the warning position based on viewport size.
        """
        if not self.is_visible:
            return

        width, height = self.engine.viewport.get_size()
        bbox = self.engine.canvas.bbox(self._text_id)
        if not bbox:
            return

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position at the top of the screen with padding
        x = width / 2
        y = self._config.padding + text_height / 2

        # Update background
        bg_width = text_width + self._config.padding * 2
        bg_height = text_height + self._config.padding
        self.engine.canvas.coords(
            self._bg_id,
            x - bg_width/2, y - bg_height/2,
            x + bg_width/2, y + bg_height/2
        )

        # Update text position
        self.engine.canvas.coords(self._text_id, x, y)