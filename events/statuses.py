from events.event import Status
from globals import *
from random import random

"""
Statuses
"""
class Burned(Status):
    """Take 10 damage at end of turn"""
    def __init__(self):
        triggers=[Trigger.END_TURN_STATUS]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.dmg=10
        self.color='red'

    def trigger(self, context):
        if context.trigger not in self.triggers or context.triggerPokemon.state!=State.ACTIVE:
            return
        context.triggerPokemon.takeDamage(dmg=self.dmg, context=context)

class Frozen(Status):
    """20% chance to escape freeze, otherwise move is skipped."""
    def __init__(self):
        triggers=[Trigger.BEFORE_MOVE]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.color='blue'
        self.unfreezeChance=0.2

    def trigger(self, context):
        if context.trigger not in self.triggers or context.attacker!=context.triggerPokemon:
            return
        if random()<self.unfreezeChance:
            context.triggerPokemon.status=None
            context.window['combatLog'].update(f'{context.triggerPokemon.name} was unfrozen!\n', append=True)
        else:
            context.cancelMove=True
            context.window['combatLog'].update(f'{context.triggerPokemon.name} is frozen and cannot move!\n', append=True)

class Paralyzed(Status):
    """Half speed. 30% chance to be unable to move"""
    def __init__(self):
        triggers=[Trigger.BEFORE_MOVE, Trigger.AFTER_STATUS]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.color='yellow'
        self.speedDebuff=0.5
        self.paraChance=0.3

    def trigger(self, context):
        if context.trigger==Trigger.BEFORE_MOVE and context.attacker==context.triggerPokemon:
            if random()<self.paraChance:
                context.cancelMove=True
                context.window['combatLog'].update(f'{context.triggerPokemon.name} was stuck in paralysis!\n', append=True)
        if context.trigger==Trigger.AFTER_STATUS and context.inflictedPokemon==context.triggerPokemon:
            context.inflictedPokemon.stats.addMult('SPE', -self.speedDebuff)
            context.window['combatLog'].update(f'{context.inflictedPokemon.name} has been slowed by paralysis!\n', append=True)

class Asleep(Status):
    """Cannot move. 30% chance to escape after each turn. Guaranteed to awake after 3 turns."""
    def __init__(self):
        triggers=[Trigger.BEFORE_MOVE]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.color='purple'
        self.turnsAsleep=1
        self.maxTurns=3
        self.wakeupChance=0.01

    def trigger(self, context):
        if context.trigger==Trigger.BEFORE_MOVE and context.attacker==context.triggerPokemon:
            if random()<self.wakeupChance or self.turnsAsleep>=self.maxTurns:
                context.window['combatLog'].update(f'{context.triggerPokemon.name} woke up!\n', append=True)
                context.triggerPokemon.status=None
                return
            context.cancelMove=True
            context.window['combatLog'].update(f'{context.triggerPokemon.name} is fast asleep!\n', append=True)
            self.turnsAsleep+=1