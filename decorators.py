from globals import *
from contexts.eventContext import *
def moveDecorator(func):
    """Decorator around move that takes in the enact function from a move class. Triggers events for before and after a move is used."""
    def wrapper(self, battleContext, moveContext):
        eventContext=MoveEventContext(moveContext=moveContext, cancelMove=False, attackMult=1)
        battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.BEFORE_MOVE)
        if not eventContext.cancelMove:
            func(self, battleContext=battleContext, moveContext=moveContext, eventContext=eventContext)
            battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.AFTER_MOVE)
        else:
            eventContext=MoveEventContext(moveContext=moveContext)
            battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.CANCELED_MOVE)
    return wrapper

def executionBehaviorDecorator(func):
    """Decorator around execution behaviors. Triggers events before execution occurs"""
    def wrapper(battleContext, moveContext, **kwargs):
        eventContext=MoveEventContext(moveContext=moveContext, cancelBehavior=False, attackMult=1)
        battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.BEFORE_EXECUTE_BEHAVIOR)
        if not eventContext.cancelBehavior:
            func(battleContext=battleContext, moveContext=moveContext, eventContext=eventContext, **kwargs)
            eventContext=MoveEventContext(moveContext=moveContext)
            battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.AFTER_EXECUTE_BEHAVIOR)
        else:
            eventContext=MoveEventContext(moveContext=moveContext)
            battleContext.eventSystem.trigger(eventContext=eventContext, trigger=Trigger.CANCELED_EXECUTE_BEHAVIOR)
    return wrapper