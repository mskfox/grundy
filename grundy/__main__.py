import os

from .nodes import MoveHistoryNode
from .core.engine import Engine
from .core.scene import Scene
from .core.events import EventType
from .nodes import GradientBackgroundNode, ParticlesNode, AtomsNode
from .nodes.game_over import GameOverNode

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "atom.ico")


class PlayScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)

        gradient = GradientBackgroundNode(
            self.engine,
            start_color="#1A1A2E",
            end_color="#16213E"
        )
        self.add_node(gradient)

        particles = ParticlesNode(
            self.engine,
            0.000035
        )
        self.add_node(particles)

        atoms = AtomsNode(self.engine)
        self.add_node(atoms)

        move_history = MoveHistoryNode(self.engine)
        self.add_node(move_history)

    def on_entry(self) -> None:
        pass

    def on_exit(self) -> None:
        pass

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


def main() -> None:
    engine = Engine()
    engine.viewport.title("Grundy's Game")
    engine.viewport.geometry("800x600")
    engine.viewport.iconbitmap(ICON_PATH)

    engine.scenes.register("play", PlayScene)
    engine.scenes.register("gameover", GameOverScene)

    engine.scenes.switch_to("play")
    engine.events.subscribe(EventType.GAME_OVER, lambda _: engine.scenes.switch_to("gameover"))

    engine.run()


if __name__ == "__main__":
    main()