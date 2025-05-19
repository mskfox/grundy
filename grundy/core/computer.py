import random
import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grundy.core.engine import Engine

class Computer:
    def __init__(self, engine: 'Engine'):
        self.engine = engine

    def think(self, delay: float = 2.0) -> tuple[bool, int, int]:
        """
        Think about the next move.
        """
        piles = self.engine.logic.piles
        splittable_piles = [pile for pile in piles.values() if pile.can_split()]
        if not splittable_piles:
            return False, None, None

        pile = random.choice(splittable_piles)
        max_position = (pile.size // 2) - 1
        position = random.randint(1, max(1, max_position))

        return True, pile.id, position