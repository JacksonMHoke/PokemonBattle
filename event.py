from abc import ABC, abstractmethod
from globals import *
from random import random

def triggerAllEvents(context, trigger):
    """Triggers all events"""
    context.trigger=trigger
    for team in context.teams:
        for trainer in team.trainers:
            for pokemon in trainer.party:
                context.triggerPokemon=pokemon
                if pokemon.item is not None:
                    pokemon.item.trigger(context)
                if pokemon.ability is not None:
                    pokemon.ability.trigger(context)
                if pokemon.status is not None:
                    pokemon.status.trigger(context)
    for event in context.events:
        event.trigger(context)
    if context.weather is not None:
        context.weather.trigger(context)

class Event(ABC):
    """
    Event that can be triggered from specific trigger

    Attributes:
        triggers (list): list of triggers that trigger event
    """
    def __init__(self, triggers):
        self.triggers=triggers

    def trigger(self, context):
        """Attempt to trigger event based on current context trigger"""
        pass

class Item(Event):
    """
    Item that triggers in battle

    Attributes:
        name (str): name of item
        timesUsed (int): number of times item has been triggered
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name
        self.timesUsed=0

class Ability(Event):
    """
    Ability that triggers in battle

    Attributes:
        name (str): name of ability
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name

class Status(Event):
    """
    Status that triggers in battle

    Attributes:
        name (str): name of status
        color (str): color of status
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name

class Weather(Event):
    """
    Weather that effects the battlefield in various ways

    Attributes:
        name (str): Name of Weather
        color (str): String name of color to display on UI
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name
        self.color='gray'

"""
Weathers
"""
class Rain(Weather):
    """Weather effect that buffs water moves by 25%."""
    def __init__(self):
        triggers=[Trigger.BEFORE_MOVE, Trigger.AFTER_MOVE, Trigger.END_TURN_STATUS]
        super().__init__(self.__class__.__name__, triggers)
        self.remainingTurns=4
        self.powerBuff=0.25
        self.buffedThisMove=False
        self.color='blue'
    
    def trigger(self, context):
        if context.trigger==Trigger.BEFORE_MOVE and context.move.type==Type.WATER:
            context.attackMult+=self.powerBuff
            context.window['combatLog'].update(f'Rain buffs the moves power by {self.powerBuff} multiplier!\n', append=True)
            self.buffedThisMove=True
        if context.trigger==Trigger.AFTER_MOVE and self.buffedThisMove:
            context.attackMult-=self.powerBuff
            self.buffedThisMove=False
        if context.trigger==Trigger.END_TURN_STATUS:
            self.remainingTurns-=1
            if self.remainingTurns<=0:
                context.window['combatLog'].update(f'Rain ended!\n', append=True)
                context.weather=None

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
        if context.trigger not in self.triggers:
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
            context.inflictedPokemon.stats[Stat.SPE]*=0.5
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
            
"""
Abilities
"""

"""
Items
"""

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self):
        triggers=[Trigger.START]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.attackBuff=10

    def trigger(self, context):
        if context.trigger not in self.triggers:
            return
        assert(self.timesUsed==0)
        context.triggerPokemon.stats[Stat.ATT]+=self.attackBuff
        self.timesUsed+=1