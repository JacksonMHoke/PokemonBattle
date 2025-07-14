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

    def attach(self, newOwner, **kwargs):
        self.buff=StatBuff(name='Sword', flat=self.buffAmount, mult=0)
        self.owner=newOwner
        self.owner.stats.addBuff(buff=self.buff, stat=self.statToBuff)
        
    def detach(self, battleContext):
        self.owner.item=None
        self.owner.stats.removeBuffs(matchById(self.buff.id), stat=self.statToBuff)
        self.owner=None

class GravityBall(Item):
    """Item that makes pokemon immune to ground type moves. The item is detached when owner is hit."""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.immunityType=Type.GROUND
        self.immuneEvent=None
        self.popEvent=None
    
    def attach(self, newOwner, **kwargs):
        self.owner=newOwner
        self.immuneEvent=TypeImmunity(immunityType=self.immunityType, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.immuneEvent)
        self.popEvent=DetachItemOnHit(item=self)
        self.battleContext.eventSystem.addPermanentEvent(self.popEvent)

    def detach(self, **kwargs):
        self.owner.item=None
        self.owner=None
        self.battleContext.eventSystem.remove(matchById(self.immuneEvent))
        self.battleContext.eventSystem.remove(matchById(self.popEvent))