from abc import ABC, abstractmethod
from globals import *
from random import random

class Event(ABC):
    """
    Event that can be triggered from specific trigger

    Attributes:
        name (str): name of event
        triggers (list[Trigger]): list of triggers that trigger event
        priority (EventPrio): Priority of event
        duration (int): Number of turns to last for
        procs (int): Number of times this event can proc
        startTurn (int):  Turn start firing the event
        id (int): Unique ID to identify event with
    """
    def __init__(self, triggers, priority=EventPrio.DEFAULT, startTurn=0, duration=1, procs=float('inf')):
        self.triggers=triggers
        self.priority=priority
        self.duration=duration
        self.procs=procs
        self.startTurn=startTurn
        self.id=getUniqueID()

    def trigger(self, battleContext, eventContext, trigger):
        """Attempt to trigger event. Returns true if event was procced, false otherwise."""
        pass

    def __lt__(self, other):
        if self.priority!=other.priority:
            return self.priority>other.priority
        return random()<0.5
    
# IDEA: Handle equipping and unequipping at the Item level instead of trying to handle it at the Event level. This way when
# for example we are swapping the sword from one pokemon to another, we just remove the buff event stored in the item and create a new
# persisting buff event for the new owner

# Create a STAT_CALC trigger that will store the stat calculations for every pokemon after the trigger
# Have the trigger function return a boolean for if the event actually did something

# Modify trainer to have a reference to the team they are on and modify pokemon to have a reference to their trainer
# Will cause a circular dependency, but will make things much much simpler in the future and will reduce the need for 
# a super bloated context class

# To handle nested triggers, have each flush of the event system to create a new EventQueue to handle everything
class Ability(Event):
    """
    Ability that triggers in battle

    Attributes:
        name (str): name of ability
        owner (Pokemon): Owner of ability
    """
    def __init__(self, name, triggers, owner=None, priority=EventPrio.ABILITY):
        super().__init__(triggers=triggers, priority=priority)
        self.name=name
        self.owner=owner

class Status(Event):
    """
    Status that triggers in battle

    Attributes:
        name (str): name of status
        color (str): color of status
    """
    def __init__(self, name, triggers, owner=None, priority=EventPrio.STATUS):
        super().__init__(triggers=triggers, priority=priority)
        self.name=name
        self.owner=owner

class Weather(Event):
    """
    Weather that effects the battlefield in various ways

    Attributes:
        name (str): Name of Weather
        color (str): String name of color to display on UI
    """
    def __init__(self, name, triggers, priority=EventPrio.WEATHER):
        super().__init__(triggers=triggers, priority=priority)
        self.name=name
        self.color='gray'