from events.event import *

class FlatStatBuff(Event):
    """
    Event that can be triggered from specific trigger to buff pokemon's flat stat

    Attributes:
        triggers (list): list of triggers that trigger event
        priority (EventPrio): Priority of event
    """
    def __init__(self, triggers, item=None, priority=EventPrio.DEFAULT):
        self.triggers=triggers
        self.priority=priority
        self.item=item
        self.name='123'

    def trigger(self, battleContext, eventContext, trigger):
        """Attempt to trigger event"""
        print('TRIGGER OF FLAT STAT BUFF', trigger in self.triggers, eventContext.item==self.item)
        if trigger in self.triggers and eventContext.item==self.item:
            self.item.owner.stats.ATT+=self.item.attackBuff

class FlatStatDebuff(Event):
    """
    Event that can be triggered from specific trigger to buff pokemon's flat stat

    Attributes:
        triggers (list): list of triggers that trigger event
        priority (EventPrio): Priority of event
    """
    def __init__(self, triggers, item=None, priority=EventPrio.DEFAULT):
        self.triggers=triggers
        self.priority=priority
        self.item=item
        self.name='1234'

    def trigger(self, battleContext, eventContext, trigger):
        """Attempt to trigger event"""
        print('TRIGGER OF FLAT STAT DEBUFF')
        if trigger in self.triggers and eventContext.item==self.item:
            print('BEFORE', self.item.owner.stats.ATT)
            self.item.owner.stats.ATT-=self.item.attackBuff
            print('AFTER', self.item.owner.stats.ATT)