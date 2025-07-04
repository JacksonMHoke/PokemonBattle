from events.event import Event
from globals import *
from random import random
from events.events import *
from items.item import Item

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self, owner):
        triggers=[Trigger.START, Trigger.EQUIP, Trigger.UNEQUIP]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.attackBuff=10

    def attach(self, battleContext):
        battleContext.eventQueue.schedule(battleContext, FlatStatBuff([Trigger.START, Trigger.EQUIP], self), Trigger.START)
        battleContext.eventQueue.schedule(battleContext, FlatStatBuff([Trigger.START, Trigger.EQUIP], self), Trigger.EQUIP)
        battleContext.eventQueue.schedule(battleContext, FlatStatDebuff([Trigger.UNEQUIP], self), Trigger.UNEQUIP)
        
    def detach(self, battleContext):
        battleContext.unsub() # TODO