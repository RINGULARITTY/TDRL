import time
from typing import List, Optional


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


class Enemy(Entity):
    def __init__(self, entityType: str, hp: float, spd: float, golds: int):
        super().__init__(-1, -1, entityType)
        self.hp: float = hp
        self.spd: float = spd
        self.golds: int = golds


class EnemyController:
    def __init__(self, enemy: Enemy, spawnTime: int):
        self.enemy: Enemy = enemy
        self.spawnTime: int = spawnTime
        self.currentWayPoint: int = 0
        self.deathSucceed: bool = True

    def Update(self, frame: int, wayPoints: list, damage: float) -> bool:
        self.enemy.hp -= damage
        if self.enemy.hp <= 0:
            self.deathSucceed = False
            return False

        if self.spawnTime > frame:
            return True
        if self.spawnTime == frame:
            self.enemy.x = wayPoints[self.currentWayPoint].x
            self.enemy.y = wayPoints[self.currentWayPoint].y
            return True

        if abs(self.enemy.x - wayPoints[self.currentWayPoint + 1].x) < 0.1 and abs(
                self.enemy.y - wayPoints[self.currentWayPoint + 1].y) < 0.1:
            self.currentWayPoint += 1
            if self.currentWayPoint >= len(wayPoints) - 1:
                return False
            self.enemy.x = wayPoints[self.currentWayPoint].x
            self.enemy.y = wayPoints[self.currentWayPoint].y

        temp = wayPoints[self.currentWayPoint + 1].x - wayPoints[self.currentWayPoint].x
        xDirection = temp / abs(temp) if temp != 0 else 0

        temp = wayPoints[self.currentWayPoint + 1].y - wayPoints[self.currentWayPoint].y
        yDirection = temp / abs(temp) if temp != 0 else 0

        self.enemy.x += xDirection * self.enemy.spd
        self.enemy.y += yDirection * self.enemy.spd

        return True


class Gobelin(Enemy):
    def __init__(self, level: int):
        super().__init__("G", 5 * level + 5, 0.5, 10)


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


class Tile:
    def __init__(self, entity: Entity):
        self.entity = entity


class GridMap:
    def __init__(self, dimensions: (int, int), wayPoints: list, entities: list):
        self.dimensions: (int, int) = dimensions
        self.wayPoints: List[WayPoint] = wayPoints
        self.entities: List[Entity] = entities

    def GetEntityAt(self, x: int, y: int) -> Optional[Entity]:
        for e in self.entities:
            if e.x == x and e.y == y:
                return e
        return None

    def GetTurgets(self) -> List[Tower]:
        return [e for e in self.entities if isinstance(e, Tower)]


class Wave:
    def __init__(self, enemyControlers):
        self.enemyControlers: List[EnemyController] = enemyControlers


class Game:
    def __init__(self, gridMap: GridMap, wave: Wave):
        self.gridMap: GridMap = gridMap
        self.wave: Wave = wave
        self.frame: int = 0
        self.golds: int = 100
        self.health: int = 10

        self.lastRewards: (float, float) = (0, 0)

    def Update(self) -> (float, float):
        self.frame += 1
        deaths = 0

        golds = self.golds
        health = self.health

        towers = self.gridMap.GetTurgets()

        for t in towers:
            t.currentShotTime += 1

        frameDamage = 0

        for i in range(len(self.wave.enemyControlers)):
            ec: EnemyController = self.wave.enemyControlers[i - deaths]
            damageDeal = 0
            for t in towers:
                if t.currentShotTime >= t.rechargeTime and abs(t.x - ec.enemy.x) < t.tRange and abs(
                        t.y - ec.enemy.y) < t.tRange:
                    t.currentShotTime = 0
                    damageDeal += t.damages
            if not ec.Update(self.frame, self.gridMap.wayPoints, damageDeal):
                if ec.deathSucceed:
                    self.health -= 1
                else:
                    self.golds += ec.enemy.golds
                self.wave.enemyControlers.pop(i - deaths)
                deaths += 1

            frameDamage += damageDeal

        strategyReward: float = 0
        if health - self.health > 0:
            winningReward = 30 * (self.health - health)
        else:
            winningReward = 2 * (self.golds - golds) + 0.1 * frameDamage

        towers = self.gridMap.GetTurgets()
        for t in towers:
            xMin = t.x - t.tRange
            yMin = t.y - t.tRange
            xMax = t.x + t.tRange
            yMax = t.y + t.tRange
            print(xMin, xMax, yMin, yMax)
            for y in range(yMin if yMin >= 0 else 0, yMax if yMax < self.gridMap.dimensions[0] else self.gridMap.dimensions[0] - 1):
                for x in range(xMin if xMin >= 0 else 0, xMax if xMax < self.gridMap.dimensions[1] else self.gridMap.dimensions[1] - 1):
                    entity: Optional[Entity] = self.gridMap.GetEntityAt(x, y)
                    if entity is not None and isinstance(entity, Way):
                        strategyReward += 1
                        print(x, y)

        strategyReward /= (len(towers) + 1)

        self.lastRewards = strategyReward, winningReward
        return self.lastRewards

    def PrintCurrentState(self):
        print(str(self.health) + "❤ " + str(self.golds) + "$")
        for i in range(self.gridMap.dimensions[0]):
            for j in range(self.gridMap.dimensions[1]):
                entityToPrint: str = "■"

                for e in self.gridMap.entities:
                    if e.GetGridPosition() == (i, j):
                        entityToPrint = e.entityType

                for e in self.wave.enemyControlers:
                    if e.enemy.GetGridPosition() == (i, j):
                        entityToPrint = e.enemy.entityType

                print(entityToPrint + " ", end="")
            print()
        print()
        print("Enemies Hp :")
        for ec in self.wave.enemyControlers:
            print("\t" + ec.enemy.entityType + str(ec.enemy.hp))
        print("Strategy rewards : " + str(self.lastRewards[0]))
        print("Winning rewards : " + str(self.lastRewards[1]))


m = GridMap((10, 10), [
        WayPoint(0, 0),
        WayPoint(2, 0),
        WayPoint(2, 9),
        WayPoint(7, 9),
        WayPoint(7, 8)
    ], [
        Start(0, 0), Way(1, 0), Way(2, 0), Way(2, 1), Way(2, 2), Way(2, 3), Way(2, 4),
        Way(2, 5), Way(2, 6), Way(2, 7), Way(2, 8), Way(2, 9), Way(3, 9), Way(4, 9),
        Way(5, 9), Way(6, 9), Way(7, 9), End(7, 8),
        Archers(1, 5)
    ]
)

w = Wave([
    EnemyController(Gobelin(50), 1),
    EnemyController(Gobelin(50), 4)
])

g = Game(m, w)
for f in range(50):
    g.Update()
    print(20 * "\n")
    g.PrintCurrentState()
    time.sleep(2)
