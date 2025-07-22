from dataclasses import dataclass
@dataclass
class MoveContext:
    def __init__(self, attackerLoc, defenderLocs, move):
        self.attacker=attackerLoc.pokemonAtSelection
        self.attackerLoc=attackerLoc
        self.defenderLocs=defenderLocs
        self.currentDefenderLoc=defenderLocs[0] if len(defenderLocs)==1 else None
        self.move=move