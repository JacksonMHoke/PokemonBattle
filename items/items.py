from events.event import Event
from events.eventUtils import *
from globals import *
from random import random
from events.events import *
from items.item import Item
from stats.statBuff import *

class Sword(Item):
    """Item that buffs attack by a flat amount"""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.buffAmount=10
        self.statToBuff='Att'

    def attach(self, newOwner):
        self.buff=StatBuff(name='Sword', flat=self.buffAmount, mult=0)
        self.owner=newOwner
        self.owner.stats.addBuff(buff=self.buff, stat=self.statToBuff)
        
    def detach(self, battleContext):
        self.owner.stats.removeBuffs(matchById(self.buff.id), stat=self.statToBuff)