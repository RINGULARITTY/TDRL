from typing import List, Optional

from entities import Entity, WayPoint
from towers import Tower


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

    def GetTowers(self) -> List[Tower]:
        return [e for e in self.entities if isinstance(e, Tower)]
