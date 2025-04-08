from abc import ABC, abstractmethod
from globals import *

def triggerAllEvents(context, trigger):                                 # TODO: Make triggerAllEvents not only trigger all items and abiltiies
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

    for event in context.events:
        event.trigger(context)

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