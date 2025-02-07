from globals import Stat
from globals import Type
from copy import deepcopy
from abc import ABC, abstractmethod
class Pokemon(ABC):
    def __init__(self, name, level, baseStats, moves, item=None, ability=None):
        self.name=name
        self.baseStats=deepcopy(baseStats)
        self.stats=deepcopy(baseStats)
        self.moves=moves
        self.ability=ability
        self.item=item
        self.fainted=False
        self.level=level
        self.exp=0

    def faint(self):
        print(f'{self.name} has fainted!', flush=True)
        self.fainted=True

    def takeDamage(self, dmg, isPhys):
        mitigation=self.stats[Stat.DEF] if isPhys else self.stats[Stat.SPD]
        self.stats[Stat.HP]-=max(dmg-self.stats[Stat.DEF], 1)
        print(f'{self.name} took {max(dmg-mitigation, 1)} damage!', flush=True)
        if self.stats[Stat.HP]<=0:
            self.faint()

class Pikachu(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.ELECTRIC]

class Rattata(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.NORMAL]