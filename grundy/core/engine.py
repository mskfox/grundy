import time

from typing import Optional

from grundy.core.canvas import Canvas
from grundy.core.events import Events, EventType
from grundy.core.logic import Logic
from grundy.core.scene import SceneManager
from grundy.core.viewport import Viewport


def _setup_on_resize_event(engine: 'Engine'):
    prev_width = None
    prev_height = None

    def _handle(event) -> None:
        nonlocal prev_width, prev_height
        width = event.width
        height = event.height

        if width != prev_width or height != prev_height:
            prev_width = width
            prev_height = height
            engine.events.emit(EventType.WINDOW_RESIZE, width, height)

    engine.viewport.bind("<Configure>", _handle)


class Engine:
    def __init__(self) -> None:
        self.viewport = Viewport()
        self.canvas = Canvas(self.viewport)
        self.events = Events()
        self.scenes = SceneManager(self)
        self.logic = Logic(self, 16)

        self._running = False
        self._last_frame_time: Optional[float] = None

        _setup_on_resize_event(self)

    def run(self) -> None:
        """Start the game engine"""
        self._running = True
        self._last_frame_time = time.time()
        self._update()
        self.viewport.mainloop()

    def stop(self) -> None:
        """Stop the game engine"""
        self._running = False
        self.viewport.quit()

    def _update(self) -> None:
        """Main update loop"""
        if not self._running:
            return

        current_time = time.time()
        delta_time = current_time - (self._last_frame_time or current_time)

        self.events.emit(EventType.UPDATE, current_time, delta_time)

        self._last_frame_time = current_time
        self.viewport.after(32, self._update)
