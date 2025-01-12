"""
Base node class for game objects
"""

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grundy.core.engine import Engine


class Node(ABC):
    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self._active = False

    @property
    def active(self) -> bool:
        """
        Check if the node is currently active in a scene
        """
        return self._active

    def _activate(self) -> None:
        """
        Internal method to activate the node
        """
        if not self._active:
            self._active = True
            self.on_activated()

    def _deactivate(self) -> None:
        """
        Internal method to deactivate the node
        """
        if self._active:
            self._active = False
            self.on_deactivated()

    def on_activated(self) -> None:
        """
        Called when the node becomes active in a scene
        """
        pass

    def on_deactivated(self) -> None:
        """
        Called when the node becomes inactive
        """
        pass