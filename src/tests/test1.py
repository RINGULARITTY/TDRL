import time

from src.environment import Environment
from src.gridmap import GridMap
from src.wave import Wave, EnemyController

from src.entities import Way, WayPoint, Start, End
from src.enemies import Goblin
from src.towers import Archers


def createSmallEmptyMap() -> None:
    gm = GridMap((5, 5), [], [])
    assert gm.dimensions[0] == 5 and gm.dimensions[1] == 5
