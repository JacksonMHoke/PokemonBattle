from globals import Stat
from globals import Type
from copy import deepcopy
from abc import ABC, abstractmethod
class Pokemon(ABC):
    """Represents Pokemon

    Attributes:
        name (str): Nickname of pokemon
        baseStats (dict): Dictionary of base stats
        stats (dict): Dictionary of current stats
        moves (list): List of moves
        ability (Ability): Pokemon's ability TODO: implement Ability class
        item (Item): Pokemon's held item TODO: implement Item class
        fainted (bool): Pokemon's fainted status TODO: implement ENUM for Fainted, Benched, Active
        level (int): Pokemon's level
        exp (int): Pokemon's EXP
        typing (list): List of types

    Note: Pokemon is an abstract class and should not be instantiated. Typing is defined in subclasses.
    """
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
        """Print fainted message and update state."""
        print(f'{self.name} has fainted!', flush=True)
        self.fainted=True

    def takeDamage(self, dmg):
        """Take damage"""
        self.stats[Stat.HP]-=dmg
        print(f'{self.name} took {dmg} damage!', flush=True)
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