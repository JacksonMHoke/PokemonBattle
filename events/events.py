from events.event import *

# Need to implement STAT_CALC and separate currHP from stats and put it in Pokemon instead.
# Have each event have a target that is static. If you want to change target you can manually,
# but best practice would be to create a new event

# I plan to separate the event logic from the stat buffing logic. I plan to beef up the stat class
# logic by having the classes store a list of buffs that we can remove by removeFn like the EventSystem
# This way we don't have to worry about copying stats and working on temporary copies, instead we can
# modify them directly and calculate the effective stats when needed. We can add buffs that last for a
# specific amount of turns and embed that in the buff list. This way the events are more distinguished
# and less all encompassing

class FlatStatBuff(Event):
    """
    Event that can be triggered from specific trigger to buff pokemon's flat stat

    Attributes:
        triggers (list): list of triggers that trigger event
        priority (EventPrio): Priority of event
    """
    def __init__(self, triggers, target=None, source=None, buffAmount=0, statToBuff='', priority=EventPrio.DEFAULT):
        self.triggers=triggers
        self.priority=priority
        self.source=source
        self.buffAmount=buffAmount if self.source is None else self.source.buffAmount
        self.statToBuff=statToBuff if self.source is None else self.source.statToBuff
        self.target=target
        self.name='FlatStatBuff'

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