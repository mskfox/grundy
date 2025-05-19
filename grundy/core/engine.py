import time

from typing import List, Optional

from grundy.core.theme import ThemeProvider
from grundy.core.canvas import Canvas
from grundy.core.computer import Computer
from grundy.core.events import Events, EventType
from grundy.core.logic import Logic
from grundy.core.scene import SceneManager
from grundy.core.viewport import Viewport


class Engine:
    def __init__(self) -> None:
        self.theme = ThemeProvider()
        self.viewport = Viewport(self)
        self.canvas = Canvas(self.viewport)
        self.events = Events()
        self.scenes = SceneManager(self)
        self.computer = Computer(self)
        self.logic = Logic(self)

        self._running = False
        self._last_frame_time: Optional[float] = None

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
