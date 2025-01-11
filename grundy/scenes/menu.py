from ..core.scene import Scene
from ..nodes.click_play import ClickPlayNode


class MenuScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)

        click_play = ClickPlayNode(self.engine)
        self.add_node(click_play)

    def on_entry(self) -> None:
        pass

    def on_exit(self) -> None:
        pass