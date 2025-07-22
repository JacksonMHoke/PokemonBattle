from events.eventSystem import EventSystem
from dataclasses import dataclass

@dataclass
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
        weather (Weather): Current weather
        eventQueue (EventQueue): Event handler
        teams (list): list of teams
    """
    def __init__(self, teams):
        self.turn=0
        self.attacker=None
        self.defender=None
        self.defenderLoc=None
        self.defenders=None
        self.attackerLoc=None
        self.defenderLocs=None
        self.move=None
        self.events=[]
        self.weather=None
        self.eventSystem=EventSystem()
        self.eventSystem.battleContext=self
        self.teams=teams
    
    def setAttacker(self, attackerLoc):
        """Updates context for new attacker"""
        self.attacker=attackerLoc.pokemonAtSelection
        self.attackerLoc=attackerLoc
    
    def setDefenders(self, defenderLocs):
        """Updates context for new defenders"""
        self.defenders=[loc.pokemon for loc in defenderLocs]
        self.defenderLocs=defenderLocs
        if len(defenderLocs)==1:
            self.defenderLoc=defenderLocs[0]
            self.defender=self.defenderLoc.pokemon
        else:
            # Defender should be specified in move enact function for more complex logic
            self.defenderLoc=None
            self.defender=None
    
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

    def attachItems(self):
        for team in self.teams:
            for trainer in team.trainers:
                for mon in trainer.party:
                    if mon.item is not None:
                        mon.item.onBattleStart()

    def attachAbilities(self):
        for team in self.teams:
            for trainer in team.trainers:
                for mon in trainer.party:
                    if mon.ability is not None:
                        mon.ability.attach(mon)