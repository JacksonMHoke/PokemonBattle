from dataclasses import dataclass

@dataclass
class EventContext:
    def __init__(self):
        self.cancelMove=False
        self.item=None
        self.attackMult=1

@dataclass
class MoveEventContext:
    def __init__(self, moveContext, **kwargs):
        self.attackerLoc=moveContext.attackerLoc
        self.attacker=moveContext.attacker
        self.defenderLoc=moveContext.currentDefenderLoc
        self.defenderLocs=moveContext.defenderLocs
        self.move=moveContext.move
        for k, v in kwargs.items():
            setattr(self, k, v)