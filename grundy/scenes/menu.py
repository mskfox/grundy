from ..core.scene import Scene
from ..nodes.gradient_background import GradientBackgroundNode
from ..nodes.flashing_text import FlashingTextNode
from ..nodes.cooling_tower import CoolingTowerNode


class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)

        gradient = GradientBackgroundNode(
            self.engine,
            start_color="skyblue",
            end_color="white"
        )
        self.add_node(gradient)

        cooling_tower1 = CoolingTowerNode(engine, 100, 500)
        self.add_node(cooling_tower1)

        cooling_tower2 = CoolingTowerNode(engine, 200, 500)
        self.add_node(cooling_tower2)

        click_play = FlashingTextNode(self.engine, "Click to play")
        self.add_node(click_play)

    def on_entry(self) -> None:
        self._onclick_id = self.engine.viewport.bind("<Button-1>", self._on_click)

    def on_exit(self) -> None:
        self.engine.viewport.unbind("<Button-1>", self._onclick_id)

    def _on_click(self, event) -> None:
        """
        Handle click events to restart the game.
        """
        self.engine.logic.reset()
        self.engine.scenes.switch_to("play")