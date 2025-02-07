from globals import Stat
from globals import Type
from abc import ABC, abstractmethod
class Pokemon(ABC):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        self.name=name
        self.stats=stats
        self.moves=moves
        self.ability=ability
        self.item=item
        self.fainted=False
        self.level=level
        self.exp=0
        self.hp=stats[Stat.MHP]
        self.speed=stats[Stat.SPE]

    def takeDamage(self, dmg):
        self.hp-=dmg
        self.fainted=self.hp<=0

class Pikachu(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.ELECTRIC]
