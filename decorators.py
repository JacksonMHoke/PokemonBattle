from globals import *
from contexts.eventContext import EventContext
def moveDecorator(func):
    """Decorator around move that takes in the enact function from a move class. Triggers events for before and after a move is used."""
    def wrapper(self, battleContext, moveContext):
        eventContext=EventContext()
        eventContext.cancelMove=False
        eventContext.attackMult=1
        battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.BEFORE_MOVE)
        if not eventContext.cancelMove:
            func(self, battleContext=battleContext, moveContext=moveContext, eventContext=eventContext)
            battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.AFTER_MOVE)
    return wrapper

def executionBehaviorDecorator(func):
    """Decorator around execution behaviors. Triggers events before execution occurs"""
    def wrapper(battleContext, moveContext, eventContext):
        eventBehaviorContext=eventContext#(eventContext) TODO: Swap to custom context
        eventBehaviorContext.cancelBehavior=False
        battleContext.eventSystem.trigger(eventContext=eventBehaviorContext, trigger=Trigger.BEFORE_EX_BEHAVIOR)
        if not eventBehaviorContext.cancelBehavior:
            func(battleContext=battleContext, moveContext=moveContext, eventContext=eventBehaviorContext)
            battleContext.eventSystem.trigger(eventContext=eventBehaviorContext, trigger=Trigger.AFTER_EX_BEHAVIOR)
    return wrapper