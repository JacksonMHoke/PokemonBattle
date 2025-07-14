from globals import *
from collections import defaultdict
from collections.abc import Iterable

class Stats:
    """Stats object that stores a pokemon's stats.
    Accessing the stats returns the mult*stat value.

    Attributes:
        baseMaxHp (int): Pokemon's base max HP
        baseAtt (int): Pokemon's base attack
        baseSpa (int): Pokemon's base special attack
        baseDef (int): Pokemon's base defense
        baseSpd (int): Pokemon's base special defense
        baseSpe (int): Pokemon's base speed
        effectiveMaxHp (int): Pokemon's effective max HP
        effectiveAtt (int): Pokemon's effective attack
        effectiveSpa (int): Pokemon's effective special attack
        effectiveDef (int): Pokemon's effective defense
        effectiveSpd (int): Pokemon's effective special defense
        effectiveSpe (int): Pokemon's effective speed
        currentHp (int): Pokemon's current hp
        buffs (Dict[str : list[StatBuff]]): Dictionary of buffs by stat

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
    """
    def __init__(self, HP=0, ATT=0, SPA=0, DEF=0, SPD=0, SPE=0):
        self.baseMaxHp=HP
        self.baseAtt=ATT
        self.baseSpa=SPA
        self.baseDef=DEF
        self.baseSpd=SPD
        self.baseSpe=SPE
        self._currentHp=HP
        self.statNames=("MaxHp", "Att", "Spa", "Def", "Spd", "Spe")
        self.buffs=defaultdict(list)

    def __setattr__(self, name, value):
        if name.startswith('effective'):
            raise AttributeError(f'{name} is a read only property and cannot be set directly.')
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        # Handles buff calculations when effectiveStat is accessed.
        if name.startswith('effective'):
            stat=name[len('effective'):]
            baseStat=self.__dict__[f'base{stat}']
            mult=1.0
            flat=0
            for buff in self.getActiveBuffs(stat):
                flat+=buff.flat
                mult+=buff.mult
            return (baseStat+flat)*mult
        # Clamps HP if currentHP is ever accessed and effectiveMaxHp is lower than it
        if name=='currentHp':
            self._currentHp=min(self._currentHp, self.effectiveMaxHp)
            return self._currentHp
        raise AttributeError(f'{self.__class__.__name__} does not have attribute {name}')
    
    def addBuff(self, buff, stat):
        """Add a buff to a stat
        
        Attributes:
            buff (StatBuff): Buff to add to stat
            stat (str): Stat to add buff to. Should be one of MaxHp, Att, Spa, Def, Spd, Spe
        """
        if stat not in self.statNames:
            raise ValueError(f"Unknown stat '{buff.stat}' in buff.")
        self.buffs[stat].append(buff)

    def removeExpiredBuffs(self, stat=None):
        """Removes expired buffs from specified stats/stat
        
        Attributes:
            stat (list[str] or str): Stat/s to remove buffs for. Handles both str and list of strs to remove from 1 or more stats    
        """
        if stat is None:
            stat=self.statNames
        if not isinstance(stat, Iterable):
            stat=[stat]
        for s in stat:
            self.buffs[s]=[buff for buff in self.buffs[s] if not buff.isExpired(self.battleContext.turn)]

    def getActiveBuffs(self, stat):
        """Gets active buffs and removes expired buffs.
        
        Attributes:
            stat (str): Stat to get active buffs for

        Returns:
            list[StatBuff]
        """
        self.removeExpiredBuffs(stat=stat)
        return [buff for buff in self.buffs[stat] if buff.isActive(self.battleContext.turn)]
    
    def removeBuffs(self, shouldRemoveFn, stat=None):
        """Removes buffs from specified stats/stat based on function passed in.
        
        Attributes:
            stat (list[str] or str): Stat/s to remove buffs for. Handles both str and list of strs to remove from 1 or more stats
            shouldRemoveFn (Callable[[StatBuff], bool]): Function used to determine whether to remove event or not
        """
        if stat is None:
            stat=self.statNames
        if not isinstance(stat, Iterable):
            stat=[stat]
        for s in stat:
            self.buffs[s]=[buff for buff in self.buffs[s] if not shouldRemoveFn(buff)]

    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, battleContext):
        """Sets battle context"""
        self._battleContext=battleContext