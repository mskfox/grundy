from ..nodes import MoveHistoryNode
from ..core.scene import Scene
from ..nodes import GradientBackgroundNode, ParticlesNode, AtomsNode


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