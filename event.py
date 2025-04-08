from abc import ABC, abstractmethod
from globals import *

def triggerAllEvents(context, trigger):
    context.trigger=trigger
    for team in context.teams:
        for trainer in team.trainers:
            for pokemon in trainer.party:
                context.triggerPokemon=pokemon
                if pokemon.item is not None:
                    pokemon.item.trigger(context)
                if pokemon.ability is not None:
                    pokemon.ability.trigger(context)

class Event(ABC):
    def __init__(self, triggers):
        self.triggers=triggers

    def trigger(self, context):
        pass

class Item(Event):
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name
        self.timesUsed=0

class Ability(Event):
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name

class Sword(Item):
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