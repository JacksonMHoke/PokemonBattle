class BattleContext:
    """
    Holds all battle context

    Attributes:
        turn (int): turn number
        attacker (Pokemon): attacking pokemon
        attackerLoc (BattleLocation): attacker location
        defenders (list): list of defending pokemon
        defenderLocs (list): list of defending pokemon locations
        move (Move): move being used right now
        events (list): list of events
        trigger (Trigger): current trigger for events
        triggerPokemon (Pokemon): current pokemon that is being triggered(ability or item)
        teams (list): list of teams
    """
    def __init__(self, teams):
        self.turn=0
        self.attacker=None
        self.defenders=None
        self.attackerLoc=None
        self.defenderLocs=None
        self.move=None
        self.events=[]
        self.weather=None
        self.trigger=None
        self.triggerPokemon=None
        self.triggerItem=None
        self.teams=teams
    
    def setAttacker(self, attackerLoc):
        """Updates context for new attacker"""
        self.attacker=attackerLoc.pokemonAtSelection
        self.attackerLoc=attackerLoc
    
    def setDefenders(self, defenderLocs):
        """Updates context for new defenders"""
        self.defenders=[loc.pokemon for loc in defenderLocs]
        self.defenderLocs=defenderLocs
    
    def addDefender(self, defender):
        """Updates context for an additional defender"""
        if self.defenders is None:
            self.defenders=[]
        self.defenders.append(defender)

    def prepareMove(self, attackerLoc, defenderLocs, move):
        """Prepares context for enacting move"""
        self.move=move
        self.setAttacker(attackerLoc)
        self.setDefenders(defenderLocs)