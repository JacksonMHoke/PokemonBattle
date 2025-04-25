from abc import ABC, abstractmethod
from globals import *
from random import random

class Event(ABC):
    """
    Event that can be triggered from specific trigger

    Attributes:
        triggers (list): list of triggers that trigger event
    """
    def __init__(self, triggers):
        self.triggers=triggers

    def trigger(self, context):
        """Attempt to trigger event based on current context trigger"""
        pass

class Item(Event):
    """
    Item that triggers in battle

    Attributes:
        name (str): name of item
        timesUsed (int): number of times item has been triggered
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name
        self.timesUsed=0

class Ability(Event):
    """
    Ability that triggers in battle

    Attributes:
        name (str): name of ability
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name

class Status(Event):
    """
    Status that triggers in battle

    Attributes:
        name (str): name of status
        color (str): color of status
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name

class Weather(Event):
    """
    Weather that effects the battlefield in various ways

    Attributes:
        name (str): Name of Weather
        color (str): String name of color to display on UI
    """
    def __init__(self, name, triggers):
        super().__init__(triggers)
        self.name=name
        self.color='gray'