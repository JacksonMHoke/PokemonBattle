from abc import ABC, abstractmethod
from globals import *
from random import random

class Event(ABC):
    """
    Event that can be triggered from specific trigger

    Attributes:
        name (str): name of event
        triggers (list): list of triggers that trigger event
        priority (EventPrio): Priority of event
    """
    def __init__(self, triggers, priority=EventPrio.DEFAULT):
        self.triggers=triggers
        self.priority=priority

    def trigger(self, battleContext, eventContext, trigger):
        """Attempt to trigger event"""
        pass

class Item(Event):
    """
    Item that triggers in battle

    Attributes:
        name (str): name of item
        owner (Pokemon): Owner of item
        timesUsed (int): number of times item has been triggered
    """
    def __init__(self, name, triggers, owner=None, priority=EventPrio.ITEM):
        super().__init__(triggers=triggers, priority=priority)
        self.name=name
        self.owner=owner
        self.timesUsed=0

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