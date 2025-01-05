from typing import List

from ...core.events import EventType
from ...core.node import Node
from .atom import Atom
from .utils import place_single_atom, NUCLEUS_RADIUS, pick_atom_at


class AtomsNode(Node):
    def __init__(self, engine):
        super().__init__(engine)
        self._tag = f"id-{id(self)}"

        self._atoms: List[Atom] = []

        self.padding = 100

        viewport_width, viewport_height = self.engine.viewport.get_size()
        self.x1, self.y1 = self.padding, self.padding
        self.x2, self.y2 = viewport_width - self.padding, viewport_height - self.padding

        self._selected_atom = None

    def on_activated(self) -> None:
        """
        Subscribe to events when active
        """
        self.engine.events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.subscribe(EventType.UPDATE, self._on_update)

        self.engine.events.subscribe(EventType.GAME_OVER, lambda : print("GAME OVER"))
        self.engine.events.subscribe(EventType.GAME_RESET, self._on_game_reset)

        self.engine.events.subscribe(EventType.PILE_ADDED, self._on_pile_added)
        self.engine.events.subscribe(EventType.PILE_REMOVED, self._on_pile_removed)

        self._onclick_id = self.engine.viewport.bind("<Button-1>", self._on_click)
        self._ondrag_id = self.engine.viewport.bind("<B1-Motion>", self._on_drag)
        self._onrelease_id = self.engine.viewport.bind("<ButtonRelease-1>", self._on_release)

        self._setup_atoms()

    def on_deactivated(self) -> None:
        """
        Clean up when node is deactivated
        """
        self.engine.events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        self.engine.events.unsubscribe(EventType.UPDATE, self._on_update)

        self.engine.events.unsubscribe(EventType.GAME_RESET, self._on_game_reset)

        self.engine.events.unsubscribe(EventType.PILE_ADDED, self._on_pile_added)
        self.engine.events.unsubscribe(EventType.PILE_REMOVED, self._on_pile_removed)

        self.engine.viewport.unbind("<Button-1>", self._onclick_id)
        self.engine.viewport.unbind("<B1-Motion>", self._ondrag_id)
        self.engine.viewport.unbind("<ButtonRelease-1>", self._onrelease_id)

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
            success, x, y = place_single_atom(self.x1, self.y1, self.x2, self.y2, self._atoms)

            if success:
                self.add_atom(x, y, pile.id, pile.size)

    def _on_click(self, event):
        clicked_atom = pick_atom_at(self._atoms, event.x, event.y)
        self._selected_atom = clicked_atom

        if self._selected_atom:
            print(self._selected_atom.size, "clicked")

    def _on_drag(self, event):
        if not self._selected_atom:
            return

        atom = self._selected_atom
        distance = ((event.x - atom.x) ** 2 + (event.y - atom.y) ** 2) ** 0.5

        distance_to_left = atom.x - self.x1
        distance_to_right = self.x2 - atom.x
        distance_to_top = atom.y - self.y1
        distance_to_bottom = self.y2 - atom.y

        max_distance_to_border = max(distance_to_left, distance_to_right, distance_to_top, distance_to_bottom)
        scaled_units = round(distance / (max_distance_to_border / atom.size))
        capped_units = min(scaled_units, atom.size)

        print(scaled_units, capped_units)

    def _on_release(self, event):
        if not self._selected_atom:
            return

        atom = self._selected_atom
        distance = ((event.x - atom.x) ** 2 + (event.y - atom.y) ** 2) ** 0.5

        distance_to_left = atom.x - self.x1
        distance_to_right = self.x2 - atom.x
        distance_to_top = atom.y - self.y1
        distance_to_bottom = self.y2 - atom.y

        max_distance_to_border = max(distance_to_left, distance_to_right, distance_to_top, distance_to_bottom)
        scaled_units = round(distance / (max_distance_to_border / atom.size))
        capped_units = min(scaled_units, atom.size)

        self.engine.logic.make_move(self._selected_atom.pile_id, capped_units)

    def _on_resize(self, width, height):
        self.x1, self.y1 = self.padding, self.padding
        self.x2, self.y2 = width - self.padding, height - self.padding
        self._setup_atoms()

    def _on_update(self, ct: float, dt: float):
        for atom in self._atoms:
            atom.update(ct, dt)

    def _on_game_reset(self):
        self._setup_atoms()

    def _on_pile_added(self, pile_id, pile_size):
        success, x, y = place_single_atom(self.x1, self.y1, self.x2, self.y2, self._atoms)
        if success:
            self.add_atom(x, y, pile_id, pile_size)

    def _on_pile_removed(self, pile_id):
        atom = self.get_atom_by_id(pile_id)
        atom.clear()
        self._atoms.remove(atom)