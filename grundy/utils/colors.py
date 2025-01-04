import re

from typing import Tuple, Union

ColorValue = Union[str, Tuple[int, int, int]]


def parse_color(color: ColorValue) -> Tuple[int, int, int]:
    """
    Parse different color formats into RGB tuple.

    Supports:
        - Hex colors: '#RGB', '#RRGGBB'
        - RGB tuples: (r, g, b)
        - Named colors: 'red', 'blue', etc.
        - RGB format: 'rgb(r, g, b)'
    """
    if isinstance(color, tuple):
        if len(color) != 3:
            raise ValueError("RGB tuple must have exactly 3 values")
        return color

    if not isinstance(color, str):
        raise ValueError(f"Invalid color format: {color}")

    # Strip whitespace and convert to lowercase
    color = color.strip().lower()

    # Handle hex colors
    if color.startswith('#'):
        color = color.lstrip('#')
        if len(color) == 3:  # Handle #RGB format
            color = ''.join(c * 2 for c in color)
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    # Handle rgb format
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
    if rgb_match:
        return tuple(int(v) for v in rgb_match.groups())

    # Handle named colors
    named_colors = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
    }

    if color in named_colors:
        return named_colors[color]

    raise ValueError(f"Invalid color format: {color}")

def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    Convert RGB tuple to hex color string
    """
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"