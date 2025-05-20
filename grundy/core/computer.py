import random

from typing import TYPE_CHECKING

from grundy.core.logic import Pile

if TYPE_CHECKING:
    from grundy.core.engine import Engine

class Computer:
    def __init__(self, engine: 'Engine'):
        self.engine = engine
        self._g_cache: dict[int, int] = {0: 0, 1: 0}

    def think(self) -> tuple[int, int]:
        piles = list(self.engine.logic.get_piles().values())

        total_xor = 0
        for p in piles:
            total_xor ^= self.pile_value(p.size)

        if total_xor == 0:
            print("No winning move (nim-sum=0), thinking randomly...")
            return self.think_random()

        for pile in piles:
            if not pile.can_split():
                continue
            g_before = self.pile_value(pile.size)
            for i in range(1, ((pile.size - 1) // 2) + 1):
                g_after = self.pile_value(i) ^ self.pile_value(pile.size - i)
                total_xor_after = total_xor ^ g_before ^ g_after
                if total_xor_after == 0:
                    print(f"Winning move found: pile {pile.id}, split into {i} and {pile.size - i}")
                    return pile.id, i

        # Shouldn't happen, but just in case.
        print("No winning move found after search, thinking randomly...")
        return self.think_random()

    def pile_value(self, n: int) -> int:
        if n in self._g_cache:
            return self._g_cache[n]

        moves = {
            self.pile_value(i) ^ self.pile_value(n - i)
            for i in range(1, ((n - 1) // 2) + 1)
        }

        g = self.mex(moves)
        self._g_cache[n] = g
        return g

    @staticmethod
    def mex(s: set[int]) -> int:
        """
        Return the minimum excludant of a set of integers.
        The minimum excludant is the smallest non-negative integer not in the set.
        :param s: The set of integers.
        :return: The minimum excludant.
        """
        m = 0
        while m in s:
            m += 1
        return m

    def think_random(self) -> tuple[int, int]:
        """
        Pick any legal split uniformly.
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
        position = random.randint(1, max(1, max_position))

        print(f"Random move: pile {pile.id}, split into {position} and {pile.size - position}")
        return pile.id, position