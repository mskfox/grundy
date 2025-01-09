from typing import Optional


class AtomWarning:
    def __init__(self, engine) -> None:
        self.engine = engine
        self.is_warning = False
        self.warning_text = "Failed to place all atoms!"
        self._tag = f"warning-{id(self)}"

        self.background_color = "#FF0000"
        self.text_color = "#FFFFFF"
        self.font = ("Arial", 12, "bold")
        self.padding = 12

        self._text_id: Optional[int] = None
        self._bg_id: Optional[int] = None

    def start_warning(self) -> None:
        """
        Start displaying a warning message.
        """
        if self.is_warning:
            return

        self.is_warning = True

        self._bg_id = self.engine.canvas.create_rectangle(
            0, 0, 0, 0,
            fill=self.background_color,
            outline="",
            tags=self._tag,
            width=2
        )

        self._text_id = self.engine.canvas.create_text(
            0, 0,
            text=self.warning_text,
            fill=self.text_color,
            font=self.font,
            tags=self._tag
        )

        self.render()

    def stop_warning(self) -> None:
        """Stop and remove the warning display."""
        if not self.is_warning:
            return

        self.engine.canvas.delete(self._tag)
        self.is_warning = False
        self._text_id = None
        self._bg_id = None

    def render(self) -> None:
        """
        Update the warning position based on viewport size.
        """
        if not self.is_warning:
            return

        width, height = self.engine.viewport.get_size()
        bbox = self.engine.canvas.bbox(self._text_id)
        if not bbox:
            return

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position at the top of the screen with padding
        x = width / 2
        y = self.padding + text_height / 2

        # Update background
        bg_width = text_width + self.padding * 2
        bg_height = text_height + self.padding
        self.engine.canvas.coords(
            self._bg_id,
            x - bg_width/2, y - bg_height/2,
            x + bg_width/2, y + bg_height/2
        )

        # Update text position
        self.engine.canvas.coords(self._text_id, x, y)