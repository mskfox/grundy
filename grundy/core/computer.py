import random
from typing import TYPE_CHECKING, Optional

from grundy.core.logic import Pile

if TYPE_CHECKING:
    from grundy.core.engine import Engine

class Computer:
    def __init__(self, engine: 'Engine'):
        self.engine = engine

        self._g_cache: dict[int, int] = {0: 0, 1: 0}
        self._cheat_mode = False

    def set_cheat_mode(self, state: bool):
        self._cheat_mode = state

    def is_cheating(self) -> bool:
        return self._cheat_mode

    def _compute_total_xor(self) -> int:
        """
        Compute the XOR (nim-sum) of Grundy values for all piles
        """
        total_xor = 0
        for pile in self.engine.logic.get_piles().values():
            total_xor ^= self._pile_value(pile.size)
        return total_xor

    def can_win(self) -> bool:
        """
        Check if computer can win by verifying if nim-sum is non-zero
        """
        return self._compute_total_xor() != 0

    def think(self) -> tuple[Optional[int], Optional[int]]:
        """
        Think of a winning move based on the current game state.
        If no winning move is found, it will think randomly.
        """
        piles = list(self.engine.logic.get_piles().values())
        total_xor = self._compute_total_xor()

        if total_xor == 0:
            print("No winning move (nim-sum=0), thinking randomly...")
            return self.think_random()

        for pile in piles:
            if not pile.can_split():
                continue

            pile_size = pile.size
            g_before = self._pile_value(pile_size)
            base = total_xor ^ g_before
            max_i = (pile_size - 1) // 2

            for i in range(1, max_i + 1):
                j = pile_size - i
                g_after = self._pile_value(i) ^ self._pile_value(j)
                if base ^ g_after == 0:
                    print(f"Winning move found: pile {pile.id}, split into {i} and {j}")
                    return pile.id, i

        print("No winning move found after search, thinking randomly...")
        return self.think_random()

    def _pile_value(self, n: int) -> int:
        """
        Compute the Grundy value for a pile of size n.
        Uses memoization to cache results for efficiency.
        """
        if n in self._g_cache:
            return self._g_cache[n]

        moves = {
            self._pile_value(i) ^ self._pile_value(n - i)
            for i in range(1, ((n - 1) // 2) + 1)
        }

        g = self._mex(moves)
        self._g_cache[n] = g
        return g

    @staticmethod
    def _mex(s: set[int]) -> int:
        """
        Compute the minimum excludant (mex) of a set of integers.
        The mex is the smallest non-negative integer not in the set.
        """
        m = 0
        while m in s:
            m += 1
        return m

    def think_random(self) -> tuple[Optional[int], Optional[int]]:
        """
        Think of a random move when no winning move is found.
        Returns a tuple of (pile_id, position) or (None, None) if no valid move exists.
        """
        print("Thinking randomly...")
        splittable = [
            p for p in self.engine.logic.get_piles().values()
            if p.can_split()
        ]

        if not splittable:
            print("No splittable piles remain.")
            return None, None

        pile = random.choice(splittable)
        max_position = (pile.size - 1) // 2
        position = random.randint(1, max_position)

        j = pile.size - position
        print(f"Random move: pile {pile.id}, split into {position} and {j}")
        return pile.id, position