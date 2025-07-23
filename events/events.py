from events.event import *
from globals import *
from random import random

class PreventMoveByChance(Event):
    """
    Event that prevents move from occuring with a specified chance.

    Attributes:
        priority (EventPrio): Priority of event
        preventChance (float): Probability to prevent move
    """
    def __init__(self, preventChance, target, triggers=[Trigger.BEFORE_MOVE], priority=EventPrio.DEFAULT, procs=float('inf')):
        super().__init__(name=self.__class__.__name__, triggers=triggers, priority=priority, procs=procs)
        self.preventChance=preventChance
        self.target=target
    
    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.BEFORE_MOVE and battleContext.attacker==self.target:
            eventContext.cancelMove=random()<self.preventChance
            return True
        return False
    
class MoveStatusByChance(TimedEvent):
    """
    Event that inflicts a pokemon with a status by chance.

    Attributes:
        status (Status): Status to inflict
        statusChance (float): Probability to status pokemon
        target (BattleLocation): Battle Location of target to inflict
    """
    def __init__(self, status, statusChance, attacker, triggers=[Trigger.AFTER_HIT], startTurn=0, duration=1, priority=EventPrio.DEFAULT, procs=float('inf')):
        super().__init__(name=self.__class__.__name__, triggers=triggers, startTurn=startTurn, duration=duration, priority=priority, procs=procs)
        self.statusChance=statusChance
        self.status=status
        self.attacker=attacker

    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.AFTER_HIT and eventContext.attacker==self.attacker:
            if random()<self.statusChance:
                eventContext.defender.inflictStatus(self.status)
            return True
        return False
    
class TypeImmunity(Event):
    """
    Event that makes a pokemon immune from all attacks of a specific type.

    Attributes:
        immunityType (Type): Type that pokemon is immune to
        immunePokemon (Pokemon): Pokemon that is immune
    """
    def __init__(self, immunityType, target, triggers=[Trigger.BEFORE_EXECUTE_BEHAVIOR], priority=EventPrio.DEFAULT, procs=float('inf')):
        super().__init__(name=self.__class__.__name__, triggers=triggers, priority=priority, procs=procs)
        self.immunityType=immunityType
        self.immunePokemon=target
    
    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.BEFORE_EXECUTE_BEHAVIOR and eventContext.defenderLoc.pokemon==self.immunePokemon and self.immunityType==eventContext.move.type:
            eventContext.cancelBehavior=True
            battleContext.window['combatLog'].update(f'{self.immunePokemon.name} is immune.\n', append=True)
            return True
        return False

class DetachItemOnHit(Event):
    """
    Event that detaches item from owner when triggered.

    Attributes:
        item (Item): Item to detach when triggered
    """
    def __init__(self, item, triggers=[Trigger.AFTER_HIT], priority=EventPrio.DEFAULT, procs=float('inf')):
        super().__init__(name=self.__class__.__name__, triggers=triggers, priority=priority, procs=procs)
        self.item=item
    
    def trigger(self, battleContext, eventContext, trigger):
        if trigger==Trigger.AFTER_HIT and eventContext.defenderLoc.pokemon==self.item.owner:
            battleContext.window['combatLog'].update(f'{self.item.name} was detached!\n', append=True)
            self.item.detach()
            return True
        return False
    
class HealPercentMaxHpIfActive(Event):
    """
    Event that heals the pokemon if they are active.
    """
    def __init__(self, healPercent, target, triggers=[], priority=EventPrio.DEFAULT, procs=float('inf')):
        super().__init__(name=self.__class__.__name__, triggers=triggers, priority=priority, procs=procs)
        self.healPercent=healPercent
        self.target=target

    def trigger(self, battleContext, eventContext, trigger):
        if trigger in self.triggers:
            healAmount=self.target.stats.effectiveMaxHp*self.healPercent
            self.target.heal(healAmount)
            return True
        return False

class EndureOHKO(Event):
    """
    Event that leaves pokemon at 1hp if they were at full hp and are being one shot. Does not work if max HP is 1.
    """
    def __init__(self, target, triggers=[Trigger.BEFORE_HIT], priority=EventPrio.SASH, procs=1):
        super().__init__(name=self.__class__.__name__, triggers=triggers, priority=priority, procs=procs)
        self.target=target

    def trigger(self, battleContext, eventContext, trigger):
        if (not hasattr(eventContext, 'defenderLoc')):
            return False
        defender=eventContext.defenderLoc.pokemon
        if trigger==Trigger.BEFORE_HIT and defender==self.target and 1<defender.stats.effectiveMaxHp<=defender.stats.currentHp<=eventContext.damage.total:
            battleContext.window['combatLog'].update(f'{defender.name} endured with 1 HP!\n', append=True)
            eventContext.damage.damageCap=defender.stats.currentHp-1
            return True
        return False