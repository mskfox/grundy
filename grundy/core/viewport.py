import tkinter as tk

from typing import Tuple


class Viewport(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._running = True

    def set_title(self, title: str) -> None:
        """
        Set the window title
        """
        self.title(title)

    def set_geometry(self, geometry: str) -> None:
        """
        Set the window geometry
        """
        self.geometry(geometry)

    def get_size(self) -> Tuple[int, int]:
        """
        Get the current window size
        """
        # processes pending events to ensure an accurate size
        self.update_idletasks()

        return self.winfo_width(), self.winfo_height()

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