from dataclasses import dataclass
@dataclass
class MoveContext:
    def __init__(self, attackerLoc, defenderLocs, move):
        self.attacker=attackerLoc.pokemonAtSelection
        self.attackerLoc=attackerLoc
        self.defenderLocs=defenderLocs
        self.currentDefenderLoc=defenderLocs[0] if len(defenderLocs)==1 else None
        self.move=move

    @property
    def attackDefenseRatio(self):
        if self.move.isPhys:
            return self.attacker.stats.effectiveAtt/self.defender.stats.effectiveDef
        else:
            return self.attacker.stats.effectiveSpa/self.defender.stats.effectiveSpd

    @property
    def defender(self):
        if self.currentDefenderLoc==None:
            return None
        return self.currentDefenderLoc.pokemon
    
    @defender.setter
    def defender(self, value):
        raise AttributeError("defender is derived from currentDefenderLoc and cannot be set directly.")