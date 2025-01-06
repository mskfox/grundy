from typing import Dict, List, TYPE_CHECKING

from .events import EventType

if TYPE_CHECKING:
    from .engine import Engine


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
    initial_pile: int
    piles: Dict[int, Pile]
    current_player: int

    def __init__(self, engine: 'Engine', initial_pile=10):
        self.engine = engine

        self.initial_pile = initial_pile
        self.reset()

    def get_piles(self) -> Dict[int, Pile]:
        return self.piles

    def get_pile(self, pile_id: int) -> Pile:
        return self.piles.get(pile_id)

    def reset(self):
        """
        Reset the game.
        """
        pile = Pile(self.initial_pile)
        self.piles = {
            pile.id: pile
        }
        self.current_player = 1
        self.engine.events.emit(EventType.GAME_RESET)

    def _abusive_reset(self):
        """
        Reset the game by creating 20 random piles.
        For testing purposes only.
        """
        import random
        self.piles = {}

        for _ in range(26):
            random_size = random.randint(1, 20)
            pile = Pile(random_size)
            self.piles[pile.id] = pile

        self.current_player = 1
        self.engine.events.emit(EventType.GAME_RESET)

    def make_move(self, pile_id: int, position: int) -> bool:
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

        self._switch_player()

        self.engine.events.emit(EventType.MOVE_MADE, pile.size, new_size1, new_size2)
        if self.is_game_over():
            self.engine.events.emit(EventType.GAME_OVER)

        return True

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

    def _switch_player(self):
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