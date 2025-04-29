from globals import *
from contexts.eventContext import EventContext
def moveDecorator(func):
    """Decorator around move that takes in the enact function from a move class. Triggers events for before and after a move is used."""
    def wrapper(self, battleContext):
        eventContext=EventContext()
        eventContext.cancelMove=False
        eventContext.attackMult=1
        battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.BEFORE_MOVE)
        if eventContext.cancelMove==False:
            func(self, battleContext=battleContext, eventContext=eventContext)
            battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.AFTER_MOVE)
    return wrapper