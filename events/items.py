from events.event import Item
from globals import *
from random import random

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self):
        triggers=[Trigger.START, Trigger.EQUIP, Trigger.UNEQUIP]
        super().__init__(name=self.__class__.__name__, triggers=triggers)
        self.attackBuff=10

    def trigger(self, context):
        if context.trigger not in self.triggers or (context.triggerItem is not None and context.triggerItem!=self):
            return
        
        if (context.trigger==Trigger.START or context.trigger==Trigger.EQUIP):
            context.triggerPokemon.stats.ATT+=self.attackBuff
        if context.trigger==Trigger.UNEQUIP:
            context.triggerPokemon.stats.ATT-=self.attackBuff

        context.triggerItem=None