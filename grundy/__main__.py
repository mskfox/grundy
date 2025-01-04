from .core import Engine
from .core import Scene
from .nodes import GradientNode, ParticlesNode


class DemoScene(Scene):
    def on_entry(self) -> None:
        gradient = GradientNode(
            self.engine,
            start_color="#1A1A2E",
            end_color="#16213E"
        )
        self.add_node(gradient)

        particles = ParticlesNode(
            self.engine,
            0.000025
        )
        self.add_node(particles)

    def on_update(self, ct: float, dt: float) -> None:
        pass

    def on_exit(self) -> None:
        pass

class EmptyScene(Scene):
    def on_entry(self) -> None:
        pass

    def on_update(self, ct: float, dt: float) -> None:
        pass

    def on_exit(self) -> None:
        pass


def main() -> None:
    engine = Engine()
    engine.viewport.set_title("Grundy's Game")
    engine.viewport.set_geometry("800x600")

    engine.scenes.register("demo", DemoScene)
    engine.scenes.register("empty", EmptyScene)

    engine.scenes.switch_to("demo")

    engine.run()


if __name__ == "__main__":
    main()