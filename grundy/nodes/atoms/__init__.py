"""
Atom simulation node for visualizing and interacting with atomic structures.
"""

from typing import List, Optional
from dataclasses import dataclass

from grundy.core.events import EventType
from grundy.core.node import Node
from grundy.nodes.atoms.atom import Atom
from grundy.nodes.atoms.utils import place_single_atom, pick_atom_at, calculate_electrons_distribution, Bounds, NUCLEUS_RADIUS
from grundy.nodes.atoms.warning import AtomWarning


@dataclass
class NodeConfig:
    """
    Configuration for the Atoms node.
    """
    padding: int = 100
    split_text_offset: int = 30  # Pixels above the atom
    split_text_font: tuple = ("Arial", 12)
    split_text_color: str = "#FFFFFF"


class AtomsNode(Node):
    """
    Node for managing atomic visualization and interaction.
    """

    def __init__(self, engine) -> None:
        """
        Initialize the atoms visualization node.
        """
        super().__init__(engine)
        self._tag = f"atoms-{id(self)}"
        self.config = NodeConfig()

        self._atoms: List[Atom] = []
        self._selected_atom: Optional[Atom] = None
        self._viewport_bounds = self._calculate_viewport_bounds()
        self._split_text_id: Optional[int] = None

        self._warning = AtomWarning(self.engine)

    def on_activated(self) -> None:
        """
        Set up event handlers when node is activated.
        """
        self._subscribe_to_events()
        self._bind_mouse_events()
        self._setup_atoms()

    def on_deactivated(self) -> None:
        """
        Clean up when node is deactivated.
        """
        self._unsubscribe_from_events()
        self._unbind_mouse_events()
        self._cleanup_atoms()

    def add_atom(self, x: int, y: int, pile_id: int, pile_size: int) -> None:
        """
        Add a new atom to the visualization.
        """
        atom = Atom(self.engine, x, y, pile_id, pile_size)
        atom.draw()
        self._atoms.append(atom)

    def get_atom_by_id(self, pile_id: int) -> Optional[Atom]:
        """
        Find an atom by its pile ID.
        """
        return next((atom for atom in self._atoms if atom.pile_id == pile_id), None)

    def _subscribe_to_events(self) -> None:
        """
        Subscribe to all required engine events.
        """
        events = self.engine.events
        events.subscribe(EventType.WINDOW_RESIZE, self._on_resize)
        events.subscribe(EventType.UPDATE, self._on_update)
        events.subscribe(EventType.GAME_RESET, self._on_game_reset)
        events.subscribe(EventType.PILE_ADDED, self._on_pile_added)
        events.subscribe(EventType.PILE_REMOVED, self._on_pile_removed)

    def _unsubscribe_from_events(self) -> None:
        """
        Unsubscribe from all engine events.
        """
        events = self.engine.events
        events.unsubscribe(EventType.WINDOW_RESIZE, self._on_resize)
        events.unsubscribe(EventType.UPDATE, self._on_update)
        events.unsubscribe(EventType.GAME_RESET, self._on_game_reset)
        events.unsubscribe(EventType.PILE_ADDED, self._on_pile_added)
        events.unsubscribe(EventType.PILE_REMOVED, self._on_pile_removed)

    def _bind_mouse_events(self) -> None:
        """
        Bind mouse event handlers.
        """
        viewport = self.engine.viewport
        self._onclick_id = viewport.bind("<Button-1>", self._on_click)
        self._ondrag_id = viewport.bind("<B1-Motion>", self._on_drag)
        self._onrelease_id = viewport.bind("<ButtonRelease-1>", self._on_release)

    def _unbind_mouse_events(self) -> None:
        """
        Unbind mouse event handlers.
        """
        viewport = self.engine.viewport
        viewport.unbind("<Button-1>", self._onclick_id)
        viewport.unbind("<B1-Motion>", self._ondrag_id)
        viewport.unbind("<ButtonRelease-1>", self._onrelease_id)

    def _cleanup_atoms(self) -> None:
        """
        Remove all atoms from the visualization.
        """
        self._remove_split_text()
        for atom in self._atoms:
            atom.clear()
        self._atoms.clear()

    def _setup_atoms(self) -> None:
        """
        Initialize atoms based on current game state.
        """
        self._cleanup_atoms()
        piles = self.engine.logic.get_piles()

        fully_successful = True
        for pile in piles.values():
            layers_quantity, _ = calculate_electrons_distribution(pile.size)
            success, x, y = place_single_atom(
                self._viewport_bounds,
                self._atoms,
                layers_quantity
            )

            if success:
                self.add_atom(x, y, pile.id, pile.size)
            else:
                self._warning.start_warning()
                fully_successful = False

        if fully_successful:
            self._warning.stop_warning()

    def _calculate_viewport_bounds(self) -> Bounds:
        """
        Calculate the viewport boundaries considering padding.
        """
        width, height = self.engine.viewport.get_size()
        return Bounds(
            self.config.padding,
            self.config.padding,
            width - self.config.padding,
            height - self.config.padding
        )

    def _calculate_split_pos(self, event_x: int, event_y: int, atom: Atom) -> int:
        """
        Calculate the split position based on drag distance.
        Only allows split up to half the size to prevent symetric duplicates.
        """
        max_allowed = (atom.size + 1) // 2

        raw_distance = ((event_x - atom.x) ** 2 + (event_y - atom.y) ** 2) ** 0.5
        adjusted_distance = max(0, raw_distance - NUCLEUS_RADIUS)

        viewport = self._viewport_bounds
        max_distance = max(
            atom.x - viewport.x1,
            viewport.x2 - atom.x,
            atom.y - viewport.y1,
            viewport.y2 - atom.y
        )

        MAX_PIXEL_PER_UNIT = 40
        effective_max_distance = min(max_distance, max_allowed * MAX_PIXEL_PER_UNIT)

        scaled_pos = round(adjusted_distance / effective_max_distance * (max_allowed - 1))
        capped_pos = min(scaled_pos, max_allowed - 1)

        return capped_pos

    def _on_click(self, event) -> None:
        """
        Handle mouse click events.
        """
        self._selected_atom = pick_atom_at(self._atoms, event.x, event.y)
        if self._selected_atom:
            self._create_split_text()

    def _on_drag(self, event) -> None:
        """
        Handle mouse drag events.
        """
        if self._selected_atom:
            units = self._calculate_split_pos(event.x, event.y, self._selected_atom)
            self._update_split_text(units)

    def _on_release(self, event) -> None:
        """
        Handle mouse release events.
        """
        if self._selected_atom:
            units = self._calculate_split_pos(event.x, event.y, self._selected_atom)
            self.engine.logic.player_move(self._selected_atom.pile_id, units)
            self._remove_split_text()
            self._selected_atom = None

    def _create_split_text(self) -> None:
        """
        Create the split text above the selected atom.
        """
        if self._selected_atom:
            self._split_text_id = self.engine.canvas.create_text(
                self._selected_atom.x,
                self._selected_atom.y - self.config.split_text_offset,
                text="",
                font=self.config.split_text_font,
                fill=self.config.split_text_color,
                tags=self._tag
            )

    def _update_split_text(self, units: int) -> None:
        """
        Update the split text with current units.
        """
        if self._split_text_id and self._selected_atom:
            self.engine.canvas.itemconfig(
                self._split_text_id,
                text=f"{self._selected_atom.size - units} | {units}"
            )
            # Update position to stay above atom
            self.engine.canvas.coords(
                self._split_text_id,
                self._selected_atom.x,
                self._selected_atom.y - self.config.split_text_offset
            )

    def _remove_split_text(self) -> None:
        """
        Remove the split text.
        """
        if self._split_text_id:
            self.engine.canvas.delete(self._split_text_id)
            self._split_text_id = None

    def _on_resize(self, _width: int, _height: int) -> None:
        """
        Handle window resize events.
        """
        self._viewport_bounds = self._calculate_viewport_bounds()
        self._setup_atoms()
        self._warning.render()

    def _on_update(self, current_time: float, delta_time: float) -> None:
        """
        Update all atoms' animations.
        """
        for atom in self._atoms:
            atom.update(current_time, delta_time)

    def _on_game_reset(self) -> None:
        """
        Handle game reset events.
        """
        self._setup_atoms()

    def _on_pile_added(self, pile_id: int, pile_size: int) -> None:
        """
        Handle new pile addition events.
        """
        layers_quantity, _ = calculate_electrons_distribution(pile_size)
        success, x, y = place_single_atom(
            self._viewport_bounds,
            self._atoms,
            layers_quantity
        )

        if success:
            self.add_atom(x, y, pile_id, pile_size)
        else:
            self._warning.start_warning()

    def _on_pile_removed(self, pile_id: int) -> None:
        """
        Handle pile removal events.
        """
        atom = self.get_atom_by_id(pile_id)
        if atom:
            atom.clear()
            self._atoms.remove(atom)