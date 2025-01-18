import random

from typing import Dict, List, TYPE_CHECKING

from grundy.core.events import EventType

if TYPE_CHECKING:
    from grundy.core.engine import Engine


class Pile:
    """
    Represents a single pile.
    """
    _size: int
    _id: int

    def __init__(self, size):
        self._size = size
        self._id = id(self)

    @property
    def id(self):
        return self._id

    @property
    def size(self):
        return self._size

    def can_split(self):
        """
        Check if the pile can be split into unequal piles.
        :return: Whether the pile can be split.
        """
        return self.size > 2


class Logic:
    _initial_piles: List[int]
    piles: Dict[int, Pile]

    current_player: int
    last_winner: int

    def __init__(self, engine: 'Engine'):
        self.engine = engine

        self._initial_piles = []
        self.last_winner = 0

        self.reset()

    def set_initial_piles(self, values: List[int]):
        """
        Set multiple initial piles.
        """
        self._initial_piles = values.copy()
        self.reset()

    def get_piles(self) -> Dict[int, Pile]:
        return self.piles

    def reset(self):
        """
        Reset the game.
        """
        self.piles = {}

        for size in self._initial_piles:
            pile = Pile(size)
            self.piles[pile.id] = pile

        self.current_player = 1
        self.engine.events.emit(EventType.GAME_RESET)

    def _make_move(self, pile_id: int, position: int) -> bool:
        """
        Make a move by splitting a pile at the given index.
        :param pile_id: The index of the pile to split.
        :param position: The position to split the pile.
        :return: Whether the move was valid.
        """
        if not self._is_valid_move(pile_id, position):
            return False

        pile = self.piles[pile_id]
        new_size1 = position
        new_size2 = pile.size - position

        del self.piles[pile_id]
        new_pile1 = Pile(new_size1)
        new_pile2 = Pile(new_size2)

        self.piles[new_pile1.id] = new_pile1
        self.piles[new_pile2.id] = new_pile2

        self.engine.events.emit(EventType.PILE_REMOVED, pile_id)
        self.engine.events.emit(EventType.PILE_ADDED, new_pile1.id, new_size1)
        self.engine.events.emit(EventType.PILE_ADDED, new_pile2.id, new_size2)

        self.engine.events.emit(EventType.MOVE_MADE, self.current_player, pile, new_pile1, new_pile2)
        if self.is_game_over():
            self.last_winner = self.current_player
            self.engine.events.emit(EventType.GAME_OVER, self.last_winner)

        self._switch_player()
        return True

    def player_move(self, pile_id: int, position: int):
        """
        Handle the player's move.
        :param pile_id: The index of the pile to split.
        :param position: The position to split the pile.
        """
        if not self.is_player_turn():
            return

        self._make_move(pile_id, position)
        self.computer_move()

    def computer_move(self) -> None:
        """
        Handles the computer's move.
        """
        if self.is_player_turn():
            return

        splittable_piles = [pile for pile in self.piles.values() if pile.can_split()]
        if not splittable_piles:
            return

        pile = random.choice(splittable_piles)

        max_position = (pile.size // 2) - 1
        position = random.randint(1, max(1, max_position))

        self._make_move(pile.id, position)

    def _is_valid_move(self, pile_id: int, position: int) -> bool:
        """
        Check if a move is valid.
        :param pile_id: The index of the pile to split.
        :param position: The position to split the pile.
        :return: Whether the move is valid.
        """
        pile = self.piles.get(pile_id)
        if not pile:
            return False

        if position <= 0 or position >= pile.size:
            return False

        new_size1 = position
        new_size2 = pile.size - position

        return new_size1 != new_size2

    def _switch_player(self) -> None:
        """
        Switch the current player.
        """
        self.current_player = 3 - self.current_player

    def is_game_over(self) -> bool:
        """
        Check if the game is over.
        :return: Whether the game is over.
        """
        return not any(pile.can_split() for pile in self.piles.values())

    def is_player_turn(self) -> bool:
        """
        Check if it is the computer's turn.
        :return: Whether it is the computer's turn.
        """
        return self.current_player == 1