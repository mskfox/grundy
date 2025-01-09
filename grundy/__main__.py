import os

from .core.engine import Engine
from .core.events import EventType
from .scenes.play import PlayScene
from .scenes.gameover import GameOverScene

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "atom.ico")


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