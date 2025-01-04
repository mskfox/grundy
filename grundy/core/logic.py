from typing import List, TYPE_CHECKING

from.events import EventType

if TYPE_CHECKING:
    from .engine import Engine


class Pile:
    """
    Represents a single pile.
    """
    size: int

    def __init__(self, size):
        self.size = size

    def can_split(self):
        """
        Check if the pile can be split into unequal piles.
        :return: Whether the pile can be split.
        """
        return self.size > 2


class Logic:
    initial_pile: int
    piles: List[Pile]
    current_player: int

    def __init__(self, engine: 'Engine', initial_pile=10):
        self.engine = engine

        self.initial_pile = initial_pile
        self.reset()

    def reset(self):
        """
        Reset the game.
        """
        self.piles = []
        self.current_player = 1
        self.engine.events.emit(EventType.GAME_RESET)

    def make_move(self, index: int, position: int) -> bool:
        """
        Make a move by splitting a pile at the given index.
        :param index: The index of the pile to split.
        :param position: The position to split the pile.
        :return: Whether the move was valid.
        """
        if not self._is_valid_move(index, position):
            return False

        pile = self.piles[index]
        new_size1 = position
        new_size2 = pile.size - position

        self.piles.pop(index)
        self.piles.append(Pile(new_size1))
        self.piles.append(Pile(new_size2))

        self._switch_player()

        self.engine.events.emit(EventType.MOVE_MADE, index, position)
        if self.is_game_over():
            self.engine.events.emit(EventType.GAME_OVER)

        return True

    def _is_valid_move(self, index: int, position: int) -> bool:
        """
        Check if a move is valid.
        :param index: The index of the pile to split.
        :param position: The position to split the pile.
        :return: Whether the move is valid.
        """
        if index >= len(self.piles):
            return False

        pile = self.piles[index]
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
        return not any(pile.can_split() for pile in self.piles)