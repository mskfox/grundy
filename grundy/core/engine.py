import time

from typing import List, Optional

from grundy.utils.palettes import PALETTES, DEFAULT_PALETTE
from grundy.core.canvas import Canvas
from grundy.core.events import Events, EventType
from grundy.core.logic import Logic
from grundy.core.scene import SceneManager
from grundy.core.viewport import Viewport


class Engine:
    def __init__(self) -> None:
        self._palette: List[str] = PALETTES[DEFAULT_PALETTE]

        self.viewport = Viewport(self)
        self.canvas = Canvas(self.viewport)
        self.events = Events()
        self.scenes = SceneManager(self)
        self.logic = Logic(self)

        self._running = False
        self._last_frame_time: Optional[float] = None

    def set_palette(self, palette_name: str) -> bool:
        """
        Set the color palette to use
        """
        if palette_name in PALETTES:
            self._palette = PALETTES[palette_name]
            return True

        print(f"Warning: Unknown palette '{palette_name}', using default.")
        return False

    @property
    def palette_size(self) -> int:
        """
        Get the number of colors in the current palette.
        """
        return len(self.current_palette)

    @property
    def current_palette(self) -> List[str]:
        """
        Get the current color palette.
        """
        if self._palette:
            return self._palette.copy()

        return PALETTES[DEFAULT_PALETTE].copy()

    def run(self) -> None:
        """
        Start the game engine
        """
        self._running = True
        self._last_frame_time = time.time()
        self._update()
        self.viewport.mainloop()

    def stop(self) -> None:
        """
        Stop the game engine
        """
        self._running = False
        self.viewport.quit()

    def _update(self) -> None:
        """
        Main update loop
        """
        if not self._running:
            return

        current_time = time.time()
        delta_time = current_time - (self._last_frame_time or current_time)

        self.events.emit(EventType.UPDATE, current_time, delta_time)

        self._last_frame_time = current_time
        self.viewport.after(32, self._update)
