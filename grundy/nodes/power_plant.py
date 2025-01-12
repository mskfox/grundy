from grundy.core.node import Node


class PowerPlantNode(Node):
    def __init__(self, engine, x, y):
        super().__init__(engine)
        self._tag = f"powerplant-{id(self)}"

        self._x, self._y = x, y

    def on_activated(self) -> None:
        self.create_power_plant()

    def on_deactivated(self) -> None:
        self.engine.canvas.delete(self._tag)

    def create_power_plant(self):
        self.create_main_building()
        self.create_chimney()
        self.create_utility_building()

    def create_main_building(self):
        pass

    def create_chimney(self):
        pass

    def create_utility_building(self):
        pass
