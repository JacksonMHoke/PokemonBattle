from events.eventSystem import EventSystem
from battle.battleQueue import BattleQueue
from contexts.eventContext import *
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
        self.events=[]
        self.weather=None
        self.battleQueue=BattleQueue()
        self.battleQueue.battleContext=self
        self.eventSystem=EventSystem()
        self.eventSystem.battleContext=self
        self.teams=teams

    def attachItems(self):
        """
        Called on battle start. Sets up all pokemon items.
        """
        for team in self.teams:
            for trainer in team.trainers:
                for mon in trainer.party:
                    if mon.item is not None:
                        mon.item.onBattleStart()

    def attachAbilities(self):
        """
        Called on battle start. Sets up all pokemon abilities.
        """
        for team in self.teams:
            for trainer in team.trainers:
                for mon in trainer.party:
                    if mon.ability is not None:
                        mon.ability.attach(mon)

    def setupBattle(self):
        self.attachItems()
        self.attachAbilities()
        self.turn=1
        self.eventSystem.trigger(eventContext=EventContext(), trigger=Trigger.START)