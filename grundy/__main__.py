import os
import sys
import argparse

from grundy.core.engine import Engine
from grundy.core.events import EventType
from grundy.scenes.play import PlayScene
from grundy.scenes.gameover import GameOverScene
from grundy.scenes.menu import MenuScene

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "atom.ico")

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for game settings.
    """
    parser = argparse.ArgumentParser(description="Grundy's Game Settings")

    parser.add_argument("--width", type=int, default=800, help="Screen width (default: 800)")
    parser.add_argument("--height", type=int, default=600, help="Screen height (default: 600)")
    parser.add_argument(
        "--pile", type=int, default=16,
        help="Set the initial pile size (default: 16)"
    )
    parser.add_argument(
        "--scene", choices=["menu", "play", "gameover"],
        default="menu",help="Choose the initial scene to start (default: 'menu')"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(args)

    engine = Engine()
    engine.viewport.title("Grundy's Game")
    engine.viewport.geometry(f"{args.width}x{args.height}")
    engine.viewport.iconbitmap(ICON_PATH)

    engine.logic.set_initial_pile(args.pile)

    engine.scenes.register("menu", MenuScene)
    engine.scenes.register("play", PlayScene)
    engine.scenes.register("gameover", GameOverScene)

    engine.scenes.switch_to(args.scene)
    engine.events.subscribe(EventType.GAME_OVER, lambda _: engine.scenes.switch_to("gameover"))

    engine.run()


if __name__ == "__main__":
    main()