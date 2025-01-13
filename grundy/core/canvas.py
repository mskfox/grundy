import tkinter as tk

from typing import Tuple, Literal, Optional, cast

from grundy.utils.colors import parse_color, rgb_to_hex, lerp_color, ColorValue, RGBColor


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
        tags: str = ""
    ) -> None:
        """
        Create a gradient effect on the canvas.
        Attention - Does not return the items ids.
        """
        start_rgb = parse_color(start_color)
        end_rgb = parse_color(end_color)

        width = bottom_right[0] - top_left[0]
        height = bottom_right[1] - top_left[1]
        steps = 100

        for i in range(steps):
            t = i / steps
            current_rgb = lerp_color(start_rgb, end_rgb, t)
            color = rgb_to_hex(current_rgb)

            if direction == "horizontal":
                x1 = top_left[0] + (width * i) // steps
                x2 = top_left[0] + (width * (i + 1)) // steps
                y1, y2 = top_left[1], bottom_right[1]
            else:
                x1, x2 = top_left[0], bottom_right[0]
                y1 = top_left[1] + (height * i) // steps
                y2 = top_left[1] + (height * (i + 1)) // steps

            self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", tags=tags)

    def create_gradient_circle(
            self,
            x: int,
            y: int,
            radius: int,
            start_color: ColorValue,
            end_color: ColorValue,
            steps: int = 50,
            tags: str = ""
    ) -> None:
        """
        Create a gradient circle (concentric circles with gradient).
        The gradient goes from the outer color (start_color) to the inner color (end_color).
        Attention - Does not return the items ids.
        """
        start_rgb = parse_color(start_color)
        end_rgb = parse_color(end_color)

        step_radius = radius // steps

        for i in range(steps):
            t = i / (steps - 1)  # t goes from 0 to 1
            current_rgb = lerp_color(start_rgb, end_rgb, t)
            color = rgb_to_hex(current_rgb)

            current_radius = radius - (step_radius * i)
            self.create_circle(x, y, current_radius, fill=color, outline="", tags=tags)

    def create_circle(
            self,
            x: int,
            y: int,
            radius: int,
            fill: ColorValue = "",
            outline: ColorValue = "",
            tags: str = ""
    ) -> int:
        """
        Create a circle on the canvas
        """
        color = "" if fill == "" else rgb_to_hex(parse_color(fill))
        outline = "" if outline == "" else rgb_to_hex(parse_color(outline))
        return self.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline=outline, tags=tags)

    def clear(self) -> None:
        """
        Clear all drawings from the canvas
        """
        self.delete("all")