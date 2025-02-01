"""
Predefined color palettes for the game.
"""

# ["#", "#", "#", "#", "#"],
PALETTES = {
    "vibrant": ["#04e762", "#f5b700", "#dc0073", "#008bf8", "#e4572e"],
    "sunset": ["#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"],
    "ocean": ["#8ecae6", "#219ebc", "#023047", "#ffb703", "#fb8500"],
    "earth": ["#606c38", "#283618", "#fefae0", "#dda15e", "#bc6c25"],
    "candy": ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"],
    "DEBUG": ["#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff"]
}

DEFAULT_PALETTE = "vibrant"

def check_palette_lengths(palettes):
    lengths = [len(colors) for colors in palettes.values()]

    # If any palette has a different length, raise an error
    if len(set(lengths)) > 1:
        raise ValueError("All palettes must have the same number of colors.")

check_palette_lengths(PALETTES)