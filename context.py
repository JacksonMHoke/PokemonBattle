class Context:
    def __init__(self, teams):
        self.turn=0
        self.attacker=None
        self.defenders=None
        self.attackerLoc=None
        self.defenderLocs=None
        self.move=None
        self.effects=[]
        self.teams=teams
    
    def setAttacker(self, attackerLoc):
        self.attacker=attackerLoc.pokemonAtSelection
        self.attackerLoc=attackerLoc
    
    def setDefenders(self, defenderLocs):
        self.defenders=[loc.pokemon for loc in defenderLocs]
        self.defenderLocs=defenderLocs
    
    def addDefender(self, defender):
        if self.defenders is None:
            self.defenders=[]
        self.defenders.append(defender)

    def prepareMove(self, attackerLoc, defenderLocs, move):
        self.move=move
        self.setAttacker(attackerLoc)
        self.setDefenders(defenderLocs)