from typing import List

from enemies import Enemy


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


class Wave:
    def __init__(self, enemiesController: List[EnemyController]):
        self.enemiesController: List[EnemyController] = enemiesController
