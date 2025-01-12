import os

from grundy.core.engine import Engine
from grundy.core.events import EventType
from grundy.scenes.play import PlayScene
from grundy.scenes.gameover import GameOverScene
from grundy.scenes.menu import MenuScene

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "atom.ico")


def main() -> None:
    engine = Engine()
    engine.viewport.title("Grundy's Game")
    engine.viewport.geometry("800x600")
    engine.viewport.iconbitmap(ICON_PATH)

    engine.scenes.register("menu", MenuScene)
    engine.scenes.register("play", PlayScene)
    engine.scenes.register("gameover", GameOverScene)

    engine.scenes.switch_to("menu")
    engine.events.subscribe(EventType.GAME_OVER, lambda _: engine.scenes.switch_to("gameover"))

    engine.run()


if __name__ == "__main__":
    main()