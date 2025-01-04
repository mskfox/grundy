import tkinter as tk

from typing import Tuple, Literal, Optional

from ..utils.colors import parse_color, rgb_to_hex, ColorValue


class Canvas(tk.Canvas):
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.pack(expand=True, fill='both')

    def create_gradient(
        self,
        start_color: ColorValue,
        end_color: ColorValue,
        top_left: Tuple[int, int],
        bottom_right: Tuple[int, int],
        direction: Literal['horizontal', 'vertical'] = "vertical",
        tag: Optional[str] = None
    ) -> None:
        """
        Create a gradient effect on the canvas
        """
        start_rgb = parse_color(start_color)
        end_rgb = parse_color(end_color)

        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        steps = 100

        for i in range(steps):
            t = i / steps
            current_rgb = tuple(
                int(start + (end - start) * t)
                for start, end in zip(start_rgb, end_rgb)
            )
            color = rgb_to_hex(current_rgb)

            if direction == "horizontal":
                x1 = top_left[0] + (width * i) // steps
                x2 = top_left[0] + (width * (i + 1)) // steps
                y1, y2 = top_left[1], bottom_right[1]
            else:
                x1, x2 = top_left[0], bottom_right[0]
                y1 = top_left[1] + (height * i) // steps
                y2 = top_left[1] + (height * (i + 1)) // steps

            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags=tag)

    def clear(self) -> None:
        """
        Clear all drawings from the canvas
        """
        self.delete("all")