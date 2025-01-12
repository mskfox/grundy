import tkinter as tk

from typing import Tuple

from grundy.core.events import EventType


class Viewport(tk.Tk):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._running = True

        self._setup_on_resize_event()

    def get_size(self) -> Tuple[int, int]:
        """
        Get the current window size
        """
        # Processes pending events to ensure an accurate size
        self.update_idletasks()
        return self.winfo_width(), self.winfo_height()

    def get_center(self) -> Tuple[int, int]:
        """
        Calculate the screen center coordinates.
        """
        width, height = self.get_size()
        return (
            width // 2,
            height //2
        )

    def _on_close(self) -> None:
        """
        Handle window close event
        """
        self._running = False
        self.quit()

    @property
    def is_running(self) -> bool:
        """
        Check if the viewport is still running
        """
        return self._running

    def _setup_on_resize_event(self):
        prev_width = None
        prev_height = None

        def _handle(event) -> None:
            nonlocal prev_width, prev_height
            width = event.width
            height = event.height

            if width != prev_width or height != prev_height:
                prev_width = width
                prev_height = height
                self.engine.events.emit(EventType.WINDOW_RESIZE, width, height)

        self.bind("<Configure>", _handle)