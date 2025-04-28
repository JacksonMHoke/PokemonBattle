from events.event import Item
from globals import *
from random import random

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self, owner):
        triggers=[Trigger.START, Trigger.EQUIP, Trigger.UNEQUIP]
        super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
        self.attackBuff=10

    def trigger(self, battleContext, eventContext, trigger):
        if trigger not in self.triggers or (eventContext.item is not None and eventContext.item!=self):
            return
        
        if (trigger==Trigger.START or trigger==Trigger.EQUIP):
            self.owner.stats.ATT+=self.attackBuff
        if trigger==Trigger.UNEQUIP:
            self.owner.stats.ATT-=self.attackBuff