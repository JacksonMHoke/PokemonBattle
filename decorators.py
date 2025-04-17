from event import *
from globals import *
def moveDecorator(func):
    """Decorator around move that takes in the enact function from a move class. Triggers events for before and after a move is used."""
    def wrapper(self, context):
        context.cancelMove=False
        triggerAllEvents(context, Trigger.BEFORE_MOVE)
        if context.cancelMove==False:
            func(self, context)
        triggerAllEvents(context, Trigger.AFTER_MOVE)
    return wrapper