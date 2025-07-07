from globals import *
from copy import deepcopy
from abc import ABC, abstractmethod

# class Stats:
#     """Stats object that stores a pokemon's stats.
#     Accessing the stats returns the mult*stat value.

#     Attributes:
#         HP (int): Pokemon's max HP
#         ATT (int): Pokemon's attack
#         SPA (int): Pokemon's special attack
#         DEF (int): Pokemon's defense
#         SPD (int): Pokemon's special defense
#         SPE (int): Pokemon's speed
#         hpMult (int): Pokemon's max HP multiplier
#         attMult (int): Pokemon's attack multiplier
#         spaMult (int): Pokemon's special attack multiplier
#         defMult (int): Pokemon's defense multiplier
#         spdMult (int): Pokemon's special defense multiplier
#         speMult (int): Pokemon's speed multiplier
#         currentHP (int): Pokemon's current HP
#     """
#     def __init__(self, HP=0, ATT=0, SPA=0, DEF=0, SPD=0, SPE=0):
#         object.__setattr__(self, 'statNames', ("HP", "ATT", "SPA", "DEF", "SPD", "SPE"))
#         object.__setattr__(self, 'currentHP', HP)
#         for stat, val in zip(self.statNames, (HP, ATT, SPA, DEF, SPD, SPE)):
#             setattr(self, f'_{stat}', val)
#             setattr(self, f'{stat.lower()}Mult', 1.0)

#     def __setattr__(self, name, value):
#         if name in self.statNames:
#             self.__dict__[f'_{name}']=value
#             return
#         object.__setattr__(self, name, value)

#     def __getattr__(self, name):
#         # only called if `name` not already in __dict__ or on the class
#         if name in self.statNames:
#             return self.__dict__[f'_{name}']*self.__dict__[f'{name.lower()}Mult']
#         raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")
    
#     def addMult(self, statName, amount):
#         """Adds multiplier to the stat specified. Pass in statName in all caps using the abbreviation for the stat"""
#         setattr(self, f'{statName.lower()}Mult', clamp(getattr(self, f'{statName.lower()}Mult')+amount, MINMULT, MAXMULT))


class Pokemon(ABC):
    """Represents Pokemon

    Attributes:
        name (str): Nickname of pokemon
        stats (Stats): Stats object that stores stats of pokemon
        currentHP (int): Current HP of pokemon
        moves (list): List of moves
        ability (Ability): Pokemon's ability
        item (Item): Pokemon's held item
        state (State): Pokemon's current state(active, benched, fainted)
        level (int): Pokemon's level
        exp (int): Pokemon's EXP
        typing (list): List of types

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
        trainer (Trainer): Owner. Will be set automatically at start of battle

    Note: Pokemon is an abstract class and should not be instantiated. Typing is defined in subclasses.
    """
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        self.name=name
        self.stats=stats
        self.moves=moves
        self.ability=ability
        self.item=item
        self.state=State.BENCHED
        self.status=None
        self.level=level
        self.exp=0

    def faint(self):
        """Print fainted message and update state."""
        print(f'{self.name} has fainted!', flush=True)
        self.state=State.FAINTED

    def heal(self, amount):
        """Heal"""
        self.stats.currentHP=min(self.stats.effectiveMaxHp, amount+self.stats.currentHP)
        self.battleContext.window['combatLog'].update(f'{self.name} healed to {self.stats.currentHP} HP!\n', append=True)

    def takeDamage(self, dmg):
        """Take damage"""
        self.stats.currentHP-=dmg
        print(f'{self.name} took {dmg} damage!', flush=True)
        self.battleContext.window['combatLog'].update(f'{self.name} took {dmg} damage!\n', append=True)
        if self.stats.currentHP<=0:
            self.faint()
            self.battleContext.window['combatLog'].update(f'{self.name} fainted!\n', append=True)

    def bindRelationships(self, trainer):
        self.trainer=trainer

    # Enforces that battleContext is set before used
    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, val):
        self._battleContext=val

    def setBattleContext(self, battleContext):
        """Sets battle context"""
        self.battleContext=battleContext
        self.stats.setBattleContext(battleContext)

    @property
    def trainer(self):
        if not hasattr(self, '_trainer') or self._trainer is None:
            raise AttributeError(f'{self.__class__.__name__} is missing trainer.')
        return self._trainer
        
    @trainer.setter
    def trainer(self, val):
        self._trainer=val

class Pikachu(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.ELECTRIC]

class Rattata(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.NORMAL]

class Bell(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.ROCK, Type.STEEL]

class Shroomhog(Pokemon):
    def __init__(self, name, level, stats, moves, item=None, ability=None):
        super().__init__(name, level, stats, moves, item, ability)
        self.typing=[Type.GROUND, Type.POISON]