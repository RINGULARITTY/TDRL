from entities import Entity


class Enemy(Entity):
    def __init__(self, entityType: str, hp: float, spd: float, golds: int):
        super().__init__(-1, -1, entityType)
        self.hp: float = hp
        self.spd: float = spd
        self.golds: int = golds


class Goblin(Enemy):
    def __init__(self, level: int):
        super().__init__("G", 5 * level + 5, 0.5, 10)