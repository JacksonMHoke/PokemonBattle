from events.event import Status
from globals import *
from random import random

"""
Statuses
"""
class Burned(Status):
    """Take 10 damage at end of turn"""
    def __init__(self, owner=None):
        triggers=[Trigger.END_TURN_STATUS]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.dmg=10
        self.color='red'

    def trigger(self, battleContext, eventContext, trigger):
        if trigger not in self.triggers or self.owner.state!=State.ACTIVE:
            return
        self.owner.takeDamage(dmg=self.dmg, battleContext=battleContext)

class Frozen(Status):
    """20% chance to escape freeze, otherwise move is skipped."""
    def __init__(self, owner=None):
        triggers=[Trigger.BEFORE_MOVE]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.color='blue'
        self.unfreezeChance=0.2

    def trigger(self, battleContext, eventContext, trigger):
        if trigger not in self.triggers or battleContext.attacker!=self.owner:
            return
        if random()<self.unfreezeChance:
            self.owner.status=None
            battleContext.window['combatLog'].update(f'{self.owner.name} was unfrozen!\n', append=True)
        else:
            eventContext.cancelMove=True
            battleContext.window['combatLog'].update(f'{self.owner.name} is frozen and cannot move!\n', append=True)

class Paralyzed(Status):
    """Half speed. 30% chance to be unable to move"""
    def __init__(self, owner=None):
        triggers=[Trigger.BEFORE_MOVE, Trigger.AFTER_STATUS]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.color='yellow'
        self.speedDebuff=0.5
        self.paraChance=0.3

    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.BEFORE_MOVE and battleContext.attacker==self.owner:
            if random()<self.paraChance:
                eventContext.cancelMove=True
                battleContext.window['combatLog'].update(f'{self.owner.name} was stuck in paralysis!\n', append=True)
        if trigger==Trigger.AFTER_STATUS and battleContext.defender==self.owner:
            self.owner.stats.addMult('SPE', -self.speedDebuff)
            battleContext.window['combatLog'].update(f'{self.owner.name} has been slowed by paralysis!\n', append=True)

class Asleep(Status):
    """Cannot move. 30% chance to escape after each turn. Guaranteed to awake after 3 turns."""
    def __init__(self, owner=None):
        triggers=[Trigger.BEFORE_MOVE]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.color='purple'
        self.turnsAsleep=1
        self.maxTurns=3
        self.wakeupChance=0.01

    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.BEFORE_MOVE and battleContext.attacker==self.owner:
            if random()<self.wakeupChance or self.turnsAsleep>=self.maxTurns:
                battleContext.window['combatLog'].update(f'{self.owner.name} woke up!\n', append=True)
                self.owner.status=None
                return
            eventContext.cancelMove=True
            battleContext.window['combatLog'].update(f'{self.owner.name} is fast asleep!\n', append=True)
            self.turnsAsleep+=1