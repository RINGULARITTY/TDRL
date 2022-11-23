from typing import Optional, List

from gridmap import GridMap
from wave import Wave, EnemyController
from entities import Entity, Way
from towers import Tower


class Environment:
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

        golds: int = self.golds
        health: int = self.health

        towers: List[Tower] = self.gridMap.GetTowers()

        for t in towers:
            t.currentShotTime += 1

        frameDamage: float = 0

        for i in range(len(self.wave.enemiesController)):
            ec: EnemyController = self.wave.enemiesController[i - deaths]
            damageDeal: float = 0
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
                self.wave.enemiesController.pop(i - deaths)
                deaths += 1

            frameDamage += damageDeal

        strategyReward: float = 0
        if health - self.health > 0:
            winningReward = 30 * (self.health - health)
        else:
            winningReward = 2 * (self.golds - golds) + 0.1 * frameDamage

        towers: List[Tower] = self.gridMap.GetTowers()
        for t in towers:
            xMin: int = int(t.x) - t.tRange
            yMin: int = int(t.y) - t.tRange
            xMax: int = int(t.x) + t.tRange
            yMax: int = int(t.y) + t.tRange
            for y in range(yMin if yMin >= 0 else 0, yMax if yMax < self.gridMap.dimensions[0] else self.gridMap.dimensions[0] - 1):
                for x in range(xMin if xMin >= 0 else 0, xMax if xMax < self.gridMap.dimensions[1] else self.gridMap.dimensions[1] - 1):
                    entity: Optional[Entity] = self.gridMap.GetEntityAt(x, y)
                    if entity is not None and isinstance(entity, Way):
                        strategyReward += 1

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

                for e in self.wave.enemiesController:
                    if e.enemy.GetGridPosition() == (i, j):
                        entityToPrint = e.enemy.entityType

                print(entityToPrint + " ", end="")
            print()
        print()
        print("Enemies Hp :")
        for ec in self.wave.enemiesController:
            print("\t" + ec.enemy.entityType + str(ec.enemy.hp))
        print("Strategy rewards : " + str(self.lastRewards[0]))
        print("Winning rewards : " + str(self.lastRewards[1]))
