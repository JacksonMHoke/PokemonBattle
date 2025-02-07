from abc import ABC, abstractmethod
from globals import Stat
from globals import Type
from actions import *
class Move(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def enact(self, context, currTrainer):
        pass

class Tackle(Move):
    def __init__(self):
        self.power=20
        self.accuracy=1
        self.critChance=0.1
        self.isPhys=True
        self.type=Type.NORMAL
        self.name=self.__class__.__name__
    def enact(self, context, currTrainer):
        singleTargetAttack.do(context, self, currTrainer)