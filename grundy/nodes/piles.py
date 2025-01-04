from ..core.events import EventType
from ..core.node import Node


class PilesNode(Node):
    def __init__(self, engine):
        super().__init__(engine)
        self._tag = f"id-{id(self)}"

    def on_activated(self) -> None:
        """
        Subscribe to events when active
        """
        self.engine.events.subscribe(EventType.MOVE_MADE, self._on_move_made)
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)

    def on_deactivated(self) -> None:
        """
        Clean up when node is deactivated
        """
        self.engine.events.unsubscribe(EventType.MOVE_MADE, self._on_move_made)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)

    def _on_update(self, ct: float, dt: float):
        pass

    def _on_move_made(self, index: int, position: int):
        pass