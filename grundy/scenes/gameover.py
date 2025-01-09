from ..core.scene import Scene
from ..nodes.gradient_background import GradientBackgroundNode
from ..nodes.game_over import GameOverNode


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

    def on_entry(self) -> None:
        pass

    def on_exit(self) -> None:
        pass