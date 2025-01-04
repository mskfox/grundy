from enum import Enum, auto
from typing import Callable, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.engine import Engine


class EventType(Enum):
    WINDOW_RESIZE = auto()
    UPDATE = auto()
    SCENE_CHANGED = auto()

    MOVE_MADE = auto()
    GAME_OVER = auto()
    GAME_RESET = auto()

    PILE_ADDED = auto()
    PILE_REMOVED = auto()


class Events:
    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}

    def subscribe(self, event_type: EventType, callback: Callable):
        """
        Subscribe to an event type with a callback function
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable) -> None:
        """
        Remove a callback from an event type's listeners
        """
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)

    def emit(self, event_type: EventType, *args, **kwargs) -> None:
        """
        Emit an event to all registered listeners
        """
        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                callback(*args, **kwargs)
