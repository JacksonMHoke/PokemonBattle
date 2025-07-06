from globals import *
from collections import defaultdict

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
        buffs (Dict[str : StatBuff]): Dictionary of buffs by stat
    """
    def __init__(self, HP=0, ATT=0, SPA=0, DEF=0, SPD=0, SPE=0):
        self.baseMaxHp=HP
        self.baseAtt=ATT
        self.baseSpa=SPA
        self.baseDef=DEF
        self.baseSpd=SPD
        self.baseSpe=SPE
        self.currentHp=HP
        self.statNames=("Hp", "Att", "Spa", "Def", "Spd", "Spe")
        self.buffs=defaultdict(list)

    def __setattr__(self, name, value):
        if name.startswith('effective'):
            raise AttributeError(f'{name} is a read only property and cannot be set directly.')
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name.startswith('effective'):
            stat=name[9:]
            baseStat=self.__dict__[f'base{stat}']
            mult=1.0
            flat=0
            for buff in self.buffs[stat]:
                flat+=buff.flat
                mult+=buff.mult
            return (baseStat+flat)*mult
        if name=='currentHp':
            return min(self.__dict__[name], self.effectiveMaxHp)
        raise AttributeError(f'{Stats.__name__} does not have attribute {name}')
    
    def addBuff(self, buff):
        self.buffs[buff.stat].append(buff)

    def removeExpiredBuffs(self):
        pass

    def getActiveBuffs(self, stat):
        pass