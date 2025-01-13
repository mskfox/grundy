import re

from typing import Tuple, Union, cast

RGBColor = Tuple[int, int, int]
ColorValue = Union[str, RGBColor]
ParsedColor = Union[str, RGBColor]


def parse_color(color: ColorValue) -> ParsedColor:
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

    if color == "":
        return ""

    # Strip whitespace and convert to lowercase
    color = color.strip().lower()

    # Handle hex colors
    if color.startswith('#'):
        color = color.lstrip('#')
        if len(color) == 3:  # Handle #RGB format
            color = ''.join(c * 2 for c in color)
        rgb_tuple = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        return cast(RGBColor, rgb_tuple)

    # Handle rgb format
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
    if rgb_match:
        rgb_tuple = tuple(int(v) for v in rgb_match.groups())
        return cast(RGBColor, rgb_tuple)

    # Handle named colors
    named_colors = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'skyblue': (135, 206, 235),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
    }

    if color in named_colors:
        return named_colors[color]

    raise ValueError(f"Invalid color format: {color}")

def rgb_to_hex(color: ParsedColor) -> str:
    """
    Convert RGB tuple to hex color string
    """
    if color == "":
        return ""
    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

def lerp_color(
        start_rgb: RGBColor,
        end_rgb: RGBColor,
        t: float
) -> RGBColor:
    """
    Linearly interpolate between two RGB colors.
    """
    return cast(RGBColor, tuple(
        int(start + (end - start) * t)
        for start, end in zip(start_rgb, end_rgb)
    ))