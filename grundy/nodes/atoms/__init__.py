from typing import List

from ...core.events import EventType
from ...core.node import Node
from .atom import Atom
from .utils import place_single_atom


class AtomsNode(Node):
    def __init__(self, engine):
        super().__init__(engine)
        self._tag = f"id-{id(self)}"

        self._atoms: List[Atom] = []

        self.padding = 60

        viewport_width, viewport_height = self.engine.viewport.get_size()
        self.x1, self.y1 = self.padding, self.padding
        self.x2, self.y2 = viewport_width - self.padding, viewport_height - self.padding

    def on_activated(self) -> None:
        """
        Subscribe to events when active
        """
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)
        self.engine.events.subscribe(EventType.GAME_RESET, self._on_game_reset)

        self.engine.events.subscribe(EventType.PILE_ADDED, self._on_pile_added)
        self.engine.events.subscribe(EventType.PILE_REMOVED, self._on_pile_removed)

        self._setup_atoms()

    def on_deactivated(self) -> None:
        """
        Clean up when node is deactivated
        """
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)
        self.engine.events.unsubscribe(EventType.GAME_RESET, self._on_game_reset)

        self.engine.events.unsubscribe(EventType.PILE_ADDED, self._on_pile_added)
        self.engine.events.unsubscribe(EventType.PILE_REMOVED, self._on_pile_removed)

        self._cleanup_atoms()

    def add_atom(self, x: int, y: int, pile_id: int, pile_size: int):
        """
        Add a single atom at the specified position (x, y).
        """
        atom = Atom(self.engine, x, y, pile_id, pile_size)
        atom.draw()
        self._atoms.append(atom)

    def get_atom_by_id(self, pile_id: int):
        for atom in self._atoms:
            if atom.pile_id == pile_id:
                return atom

    def _cleanup_atoms(self):
        for atom in self._atoms:
            atom.clear()
        self._atoms.clear()

    def _setup_atoms(self):
        self._cleanup_atoms()
        piles = self.engine.logic.get_piles()

        for pile in piles.values():
            x, y = place_single_atom(self.x1, self.y1, self.x2, self.y2, self._atoms)

            if x is not None and y is not None:
                self.add_atom(x, y, pile.id, pile.size)

    def _on_update(self, ct: float, dt: float):
        for atom in self._atoms:
            atom.update(ct, dt)

    def _on_game_reset(self):
        self._setup_atoms()

    def _on_pile_added(self, pile_id, pile_size):
        x, y = place_single_atom(self.x1, self.y1, self.x2, self.y2, self._atoms)
        if x is not None and y is not None:
            self.add_atom(x, y, pile_id, pile_size)

    def _on_pile_removed(self, pile_id):
        atom = self.get_atom_by_id(pile_id)
        atom.clear()
        self._atoms.remove(atom)