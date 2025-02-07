from globals import Stat
from globals import Type
from abc import ABC, abstractmethod
class Move(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def enact(self, context):
        pass

class Tackle(Move):
    def __init__(self):
        self.power=20
        self.accuracy=100
        self.critChance=0.1
    def enact(self, context):
        pass