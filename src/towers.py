from src.entities import Entity


class Tower(Entity):
    def __init__(self, x, y, entityType, tRange, rechargeTime, damages, price):
        super().__init__(x, y, entityType)
        self.tRange: int = tRange
        self.rechargeTime: int = rechargeTime
        self.currentShotTime: int = 0
        self.damages: float = damages
        self.price: int = price


class Archers(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "A", 3, 1, 5, 50)


class Magic(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, "M", 4, 5, 30, 75)