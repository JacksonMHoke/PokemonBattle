from events.event import *
from globals import *
from random import random

class PreventMoveByChance(Event):
    """
    Event that prevents move from occuring with a specified chance.

    Attributes:
        triggers (list): List of triggers that trigger event
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