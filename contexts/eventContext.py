from dataclasses import dataclass

@dataclass
class EventContext:
    def __init__(self):
        self.cancelMove=False
        self.item=None
        self.attackMult=1

@dataclass
class AfterHitEventContext:
    def __init__(self, attackerLoc, defenderLoc, attacker, defender, move, dmg):
        self.attackerLoc=attackerLoc
        self.defenderLoc=defenderLoc
        self.attacker=attacker
        self.defender=defender
        self.move=move
        self.dmg=dmg