from random import random
from globals import *
from gui import *

class EventAction:
    """Represents an action in battle.

    This class is a parent class to various different event actions. The order starts with
    events scheduled for the lowest turn, and then picks the highest priority event. In cases
    of a tie the order is random.

    Attributes:
        event (Event): Event to trigger
        turn (int): turn number
        priority (int): priority value
    """
    def __init__(self, event, turn, priority):
        self.turn=turn
        self.priority=priority
        self.event=event
    
    def __lt__(self, other):
        if self.turn!=other.turn:
            return self.turn<other.turn
        if self.priority!=other.priority:
            return self.priority>other.priority
        return random()<0.5
    
    def execute(self, context, eventContext, trigger):
        """Execute event"""
        self.event.trigger(self, context, eventContext, trigger)