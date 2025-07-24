from events.event import Event
from utils import *
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

    def onBattleStart(self):
        self.buff=StatBuff(name='Sword', flat=self.buffAmount, mult=0)
        self.owner.stats.addBuff(buff=self.buff, stat=self.statToBuff)

    def attach(self, newOwner, **kwargs):
        super().attach(newOwner=newOwner)
        self.buff=StatBuff(name='Sword', flat=self.buffAmount, mult=0)
        self.owner.stats.addBuff(buff=self.buff, stat=self.statToBuff)
        
    def detach(self, battleContext):
        self.owner.stats.removeBuffs(matchById(self.buff.id), stat=self.statToBuff)
        super().detach()

class GravityBall(Item):
    """Item that makes pokemon immune to ground type moves. The item is detached when owner is hit."""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.immunityType=Type.GROUND
        self.immuneEvent=None
        self.popEvent=None

    def onBattleStart(self):
        self.immuneEvent=TypeImmunity(immunityType=self.immunityType, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.immuneEvent)
        self.popEvent=DetachItemOnHit(item=self)
        self.battleContext.eventSystem.addPermanentEvent(self.popEvent)
    
    def attach(self, newOwner, **kwargs):
        super().attach(newOwner=newOwner)
        self.immuneEvent=TypeImmunity(immunityType=self.immunityType, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.immuneEvent)
        self.popEvent=DetachItemOnHit(item=self)
        self.battleContext.eventSystem.addPermanentEvent(self.popEvent)

    def detach(self, **kwargs):
        self.battleContext.eventSystem.remove(matchById(self.immuneEvent))
        self.immuneEvent=None
        self.battleContext.eventSystem.remove(matchById(self.popEvent))
        self.popEvent=None
        super().detach()

class GreenFungus(Item):
    """Item that heals owner 1/16 of the user's HP at the end of every turn"""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.healPercent=1/16

    def onBattleStart(self):
        self.healEvent=HealPercentMaxHpIfActive(healPercent=self.healPercent, target=self.owner, triggers=[Trigger.END_TURN])
        self.battleContext.eventSystem.addPermanentEvent(self.healEvent)
    
    def attach(self, newOwner, **kwargs):
        super().attach(newOwner=newOwner)
        self.healEvent=HealPercentMaxHpIfActive(healPercent=self.healPercent, target=self.owner, triggers=[Trigger.END_TURN])
        self.battleContext.eventSystem.addPermanentEvent(self.healEvent)

    def detach(self, **kwargs):
        self.battleContext.eventSystem.remove(matchById(self.healEvent))
        self.healEvent=None
        super().detach()

class FocusSash(Item):
    """Leaves pokemon at 1HP if they are about to be OHKO from full hp."""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)

    def onBattleStart(self):
        self.surviveEvent=EndureOHKO(self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.surviveEvent)

    def attach(self, newOwner):
        super().attach(newOwner=newOwner)
        self.surviveEvent=EndureOHKO(self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.surviveEvent)

    def detach(self):
        self.battleContext.eventSystem.remove(matchById(self.surviveEvent))
        self.surviveEvent=None
        super().detach()

class ExpertBelt(Item):
    """Boosts the power of super effective moves by 20%"""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.attackMult=0.2

    def onBattleStart(self):
        self.boostEvent=DamageBoostSuperEff(basePowerBoost=0, attackMult=self.attackMult, flatBoost=0, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.boostEvent)

    def attach(self, newOwner):
        super().attach(newOwner=newOwner)
        self.boostEvent=DamageBoostSuperEff(basePowerBoost=0, attackMult=self.attackMult, flatBoost=0, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.boostEvent)

    def detach(self):
        self.battleContext.eventSystem.remove(matchById(self.boostEvent))
        self.boostEvent=None
        super().detach()

class Metronome(Item):
    """Moves used repeatedly gain power, stacking up to 100% bonus after 5 uses."""
    def __init__(self, owner):
        super().__init__(name=self.__class__.__name__, owner=owner)
        self.attackMult=0.25
        self.maxRepeats=4

    def onBattleStart(self):
        self.boostEvent=RepeatedMoveRampingDamage(basePowerIncrement=0, attackMultIncrement=self.attackMult, flatBoostIncrement=0, maxRepeats=self.maxRepeats, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.boostEvent)

    def attach(self, newOwner):
        super().attach(newOwner=newOwner)
        self.boostEvent=RepeatedMoveRampingDamage(basePowerIncrement=0, attackMultIncrement=self.attackMult, flatBoostIncrement=0, maxRepeats=self.maxRepeats, target=self.owner)
        self.battleContext.eventSystem.addPermanentEvent(self.boostEvent)

    def detach(self):
        self.battleContext.eventSystem.remove(matchById(self.boostEvent))
        self.boostEvent=None
        super().detach()