import random

from typing import Dict, List, TYPE_CHECKING

from grundy.core.events import EventType

if TYPE_CHECKING:
    from grundy.core.engine import Engine

RANDOM_RESET_MIN_QUANTITY = 1
RANDOM_RESET_MAX_QUANTITY = 4
RANDOM_RESET_MIN_SIZE = 3
RANDOM_RESET_MAX_SIZE = 10


class Pile:
    """
    Represents a single pile.
    """
    _id: int
    _size: int
    _kind: int

    def __init__(self, size, kind = 0):
        self._id = id(self)
        self._size = size
        self._kind = kind

    @property
    def id(self):
        return self._id

    @property
    def size(self):
        return self._size

    @property
    def kind(self):
        return self._kind

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

    def set_initial_piles(self, values: List[int]):
        """
        Set multiple initial piles.
        """
        self._initial_piles = [] if values is None else values.copy()
        self.reset()

    def get_piles(self) -> Dict[int, Pile]:
        return self.piles

    def _random_reset(self):
        """
        Performs a reset with random piles.
        """
        num_piles = random.randint(RANDOM_RESET_MIN_QUANTITY, RANDOM_RESET_MAX_QUANTITY)
        for _ in range(num_piles):
            kind = random.randint(0, self.engine.theme.size - 1)
            pile = Pile(random.randint(RANDOM_RESET_MIN_SIZE, RANDOM_RESET_MAX_SIZE), kind)
            self.piles[pile.id] = pile

    def _custom_reset(self):
        """
        Performs a reset with predefined piles.
        """
        for size in self._initial_piles:
            kind = random.randint(0, self.engine.theme.size - 1)
            pile = Pile(size, kind)
            self.piles[pile.id] = pile

    def reset(self):
        """
        Reset the game.
        """
        self.piles = {}

        if self._initial_piles:
            self._custom_reset()
        else:
            self._random_reset()


        if self.engine.computer.is_cheating():
            self.current_player = 2 if self.engine.computer.can_win() else 1
        else:
            self.current_player = random.randint(1, 2)

        self.engine.events.emit(EventType.GAME_RESET)

        if self.current_player == 2:
            self.computer_move()

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
        new_pile1 = Pile(new_size1, pile.kind)
        new_pile2 = Pile(new_size2, pile.kind)

        self.piles[new_pile1.id] = new_pile1
        self.piles[new_pile2.id] = new_pile2

        self.engine.events.emit(EventType.PILE_REMOVED, pile_id)
        self.engine.events.emit(EventType.PILE_ADDED, new_pile1)
        self.engine.events.emit(EventType.PILE_ADDED, new_pile2)

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

        pile_id, position = self.engine.computer.think()
        if pile_id is None or position is None:
            return

        self.engine.canvas.after(
            400, self._make_move,
            pile_id, position
        )

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