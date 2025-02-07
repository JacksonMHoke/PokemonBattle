from globals import Type
from globals import Stat
from globals import getEffectiveness
from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def do(self, context):
        pass

class singleTargetAttack(Action):
    def do(self, context):
        pass