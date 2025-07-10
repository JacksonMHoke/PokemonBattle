# from events.event import Item
# from events.events import *
# from globals import *
# from random import random

# class Sword(Item):
#     """Item that buffs attack by a flat amount"""
#     def __init__(self, owner):
#         triggers=[Trigger.START, Trigger.EQUIP, Trigger.UNEQUIP]
#         super().__init__(name=self.__class__.__name__, triggers=triggers, owner=owner)
#         self.attackBuff=10

#     def trigger(self, battleContext, eventContext, trigger):
#         pass
#         # if trigger not in self.triggers or (eventContext.item is not None and eventContext.item!=self):
#         #     return
        
#         # if (trigger==Trigger.START or trigger==Trigger.EQUIP):
#         #     self.owner.stats.ATT+=self.attackBuff
#         # if trigger==Trigger.UNEQUIP:
#         #     self.owner.stats.ATT-=self.attackBuff

#     def schedule(self, battleContext, trigger=None):
#         print('BEING SCHEDULED')
#         battleContext.eventQueue.schedule(battleContext, FlatStatBuff([Trigger.START, Trigger.EQUIP], self), Trigger.START)
#         battleContext.eventQueue.schedule(battleContext, FlatStatBuff([Trigger.START, Trigger.EQUIP], self), Trigger.EQUIP)
#         battleContext.eventQueue.schedule(battleContext, FlatStatDebuff([Trigger.UNEQUIP], self), Trigger.UNEQUIP)