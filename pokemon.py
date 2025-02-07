from globals import Stat
from globals import Type
from abc import ABC, abstractmethod
class Pokemon(ABC):
    def __init__(self, name, typing, level, stats, moves, item=None, ability=None):
        self.name=name
        self.typing=typing
        self.stats=stats
        self.moves=moves
        self.ability=ability
        self.item=item
        self.fainted=False
        self.level=level
        self.exp=0
        self.hp=stats[Stat.MHP]
        self.speed=stats[Stat.SPE]

    