from ..core.scene import Scene
from ..nodes.gradient_background import GradientBackgroundNode
from ..nodes.game_over import GameOverNode
from ..nodes.flashing_text import FlashingTextNode


class GameOverScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)

        gradient = GradientBackgroundNode(
            self.engine,
            start_color="#FF4E50",
            end_color="#414345"
        )
        self.add_node(gradient)

        game_over = GameOverNode(self.engine)
        self.add_node(game_over)

        click_play = FlashingTextNode(self.engine, "Click to play again")
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