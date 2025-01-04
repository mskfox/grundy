"""
Scene management for the Grundy game engine
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Type, TYPE_CHECKING

from .events import EventType
from .node import Node

if TYPE_CHECKING:
    from .engine import Engine


class Scene(ABC):
    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self.nodes: List[Node] = []
        self._active = False

    def add_node(self, node: Node) -> None:
        """
        Add a node to the scene
        """
        self.nodes.append(node)
        if self._active:
            node._activate()

    def remove_node(self, node: Node) -> None:
        """
        Remove a node from the scene
        """
        if node in self.nodes:
            if self._active:
                node._deactivate()
            self.nodes.remove(node)

    def _activate(self) -> None:
        """
        Internal method to activate the scene and its nodes
        """
        self._active = True
        for node in self.nodes:
            node._activate()
        self.on_entry()

    def _deactivate(self) -> None:
        """
        Internal method to deactivate the scene and its nodes
        """
        self._active = False
        for node in self.nodes:
            node._deactivate()
        self.on_exit()

    @abstractmethod
    def on_entry(self) -> None:
        """
        Called when the scene becomes active
        """
        pass

    @abstractmethod
    def on_exit(self) -> None:
        """
        Called when the scene is deactivated
        """
        pass


class SceneManager:
    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self._scenes: Dict[str, Scene] = {}
        self._current_scene: Optional[Scene] = None

    def register(self, name: str, scene_class: Type[Scene]) -> None:
        """Register a new scene class with a name"""
        scene = scene_class(self.engine)
        self._scenes[name] = scene

    def switch_to(self, name: str) -> None:
        """Switch to a different scene"""
        if name not in self._scenes:
            raise KeyError(f"Scene '{name}' not registered")

        if self._current_scene:
            self._current_scene._deactivate()

        self._current_scene = self._scenes[name]
        self._current_scene._activate()

        self.engine.events.emit(EventType.SCENE_CHANGED, name)

    @property
    def current(self) -> Optional[Scene]:
        """Get the current active scene"""
        return self._current_scene