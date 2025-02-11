from abc import ABC, abstractmethod
from random import random
from globals import *
class BattleAction(ABC):
    def __init__(self, turn, priority, speed):
        self.turn=turn
        self.priority=priority
        self.speed=speed
    
    def __lt__(self, other):
        if self.turn!=other.turn:
            return self.turn<other.turn
        if self.priority!=other.priority:
            return self.priority<other.priority
        if self.speed!=other.speed:
            return self.speed<other.speed
        return random()<0.5
    
class BattleLocation:
    def __init__(self, teamIdx, slotIdx, pokemon):
        self.team=teamIdx
        self.slot=slotIdx
        self.pokemonAtCreation=pokemon
    def resolve(self, context):
        return context['team'][self.team].slots[self.slot]
    
class MoveAction(BattleAction):
    def __init__(self, turn, move, attacker, targetLocs):
        super().__init__(turn, move.priority, attacker.stats[Stat.SPE])
        self.move=move
        self.attacker=attacker
        self.targetLocs=targetLocs
    def execute(self, context):
        self.move.enact(context, self.targetReqs)