import os
import argparse

from grundy.core.engine import Engine
from grundy.core.events import EventType
from grundy.scenes.play import PlayScene
from grundy.scenes.gameover import GameOverScene
from grundy.scenes.menu import MenuScene

ICON_PATH = os.path.join(os.path.dirname(__file__), "assets", "atom.ico")

def pilesize(value):
    """
    Custom type for argparse that ensures pile sizes are at least 3.
    """
    ivalue = int(value)
    if ivalue < 3:
        raise argparse.ArgumentTypeError(f"Pile size must be at least 3 (got {ivalue})")
    return ivalue

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for game settings.
    """
    parser = argparse.ArgumentParser(description="Grundy's Game Settings")

    parser.add_argument("--width", type=int, default=800, help="set the initial screen width (default: 800)")
    parser.add_argument("--height", type=int, default=600, help="set the initial screen height (default: 600)")
    parser.add_argument(
        "--piles", "-p", type=pilesize, nargs="+", default=[8, 8],
        help="set multiple initial pile sizes (e.g., --piles 7 5 3)"
    )
    parser.add_argument(
        "--scene", choices=["menu", "play", "gameover"],
        default="menu",help="choose the initial scene to start (default: 'menu')"
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(args)

    engine = Engine()
    engine.viewport.title("Grundy's Game")
    engine.viewport.geometry(f"{args.width}x{args.height}")

    if os.path.exists(ICON_PATH):
        engine.viewport.iconbitmap(ICON_PATH)
    else:
        print(f"Warning: Icon file not found at {ICON_PATH}, using default icon.")

    engine.logic.set_initial_piles(args.piles)

    engine.scenes.register("menu", MenuScene)
    engine.scenes.register("play", PlayScene)
    engine.scenes.register("gameover", GameOverScene)

    engine.scenes.switch_to(args.scene)
    engine.events.subscribe(EventType.GAME_OVER, lambda _: engine.scenes.switch_to("gameover"))

    engine.run()


if __name__ == "__main__":
    main()