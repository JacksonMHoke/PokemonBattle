from abc import ABC, abstractmethod
from globals import *
from behaviors import *
from battleaction import *
class Move(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def enact(self, context, attackerLoc, targetLocs):
        pass
    @abstractmethod
    def select(self, context, attackerLoc):
        pass

class Tackle(Move):
    def __init__(self):
        self.power=20
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.NORMAL
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLocLoc):
        return SelectSingleTarget.select(context, attackerLocLoc)

class Earthquake(Move):
    def __init__(self):
        self.power=100
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.GROUND
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)

class Thunder(Move):
    def __init__(self):
        self.power=120
        self.accuracy=0.7
        self.critChance=CRITCHANCE
        self.isPhys=False
        self.type=Type.ELECTRIC
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLocLoc):
        return SelectSingleTarget.select(context, attackerLocLoc)