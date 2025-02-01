from typing import List

from grundy.utils.palettes import PALETTES, DEFAULT_PALETTE


class ThemeProvider:
    def __init__(self):
        self._current_palette: List[str] = PALETTES[DEFAULT_PALETTE]

    def set(self, name: str) -> bool:
        """
        Set the color palette to use
        """
        if name in PALETTES:
            self._current_palette = PALETTES[name]
            return True

        return False

    @property
    def size(self) -> int:
        """
        Get the number of colors in the current palette.
        """
        return len(self.current)

    @property
    def current(self) -> List[str]:
        """
        Get the current color palette.
        """
        if self._current_palette:
            return self._current_palette.copy()

        return PALETTES[DEFAULT_PALETTE].copy()