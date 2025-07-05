from events.event import Event
from events.eventUtils import *
from globals import *
from random import random
from events.events import *
from items.item import Item

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self, owner):
        triggers=[Trigger.STAT_CALC]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.buff=10

    def attach(self, battleContext):
        self.buffEvent=FlatStatBuff()
        battleContext.eventSystem.addPermanentEvent(self.buffEvent)
        
    def detach(self, battleContext):
        battleContext.eventSystem.remove(matchById(self.buffEvent), self.triggers)