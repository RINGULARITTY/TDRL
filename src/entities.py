class Entity:
    def __init__(self, x: float, y: float, entityType: str):
        self.x: float = x
        self.y: float = y
        self.entityType: str = entityType

    def GetGridPosition(self) -> (int, int):
        return int(self.x), int(self.y)


class Way(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, "□")


class Start(Way):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.entityType = "◪"


class End(Way):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.entityType = "◩"


class WayPoint(Entity):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, "")