import time

from environment import Environment
from gridmap import GridMap
from wave import Wave, EnemyController

from entities import Way, WayPoint, Start, End
from enemies import Goblin
from towers import Archers

if __name__ == "__main__":
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
        EnemyController(Goblin(50), 1),
        EnemyController(Goblin(50), 4)
    ])

    env = Environment(m, w)
    for f in range(50):
        env.Update()
        print(20 * "\n")
        env.PrintCurrentState()
        time.sleep(2)
