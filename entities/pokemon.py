from globals import *
from copy import deepcopy
from abc import ABC, abstractmethod

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
        self.stats.currentHp=min(self.stats.effectiveMaxHp, amount+self.stats.currentHp)
        self.battleContext.window['combatLog'].update(f'{self.name} healed to {self.stats.currentHp} HP!\n', append=True)

    def takeDamage(self, dmg):
        """Take damage"""
        self.stats.currentHp-=dmg
        print(f'{self.name} took {dmg} damage!', flush=True)
        self.battleContext.window['combatLog'].update(f'{self.name} took {dmg} damage!\n', append=True)
        if self.stats.currentHp<=0:
            self.faint()
            self.battleContext.window['combatLog'].update(f'{self.name} fainted!\n', append=True)

    def inflictStatus(self, status):
        """Inflict status"""
        self.status=status
        status.inflictStatus(pokemon=self, battleContext=self.battleContext)

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