from abc import ABC, abstractmethod
from globals import *

class Status(ABC):
    """Status effect class

    Attributes:
        id (int): Unique ID
        name (str): Name of status
        color (str): Color to display status
        inflictedPokemon (Pokemon): The pokemon inflicted by the status
    """
    def __init__(self, name, color='gray'):
        self.id=getUniqueID()
        self.color=color
        self.name=name

    @abstractmethod
    def inflictStatus(self, pokemon, battleContext):
        """Takes in a pokemon and inflicts it with this status."""
        pass

    @abstractmethod
    def cureStatus(self, battleContext):
        """Cures the current inflicted pokemon of its statuses"""
        pass