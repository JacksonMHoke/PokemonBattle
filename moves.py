from abc import ABC, abstractmethod
from globals import *
from behaviors import *
from battleaction import *
class Move(ABC):
    """Abstract class for moves.

    This is an abstract class that requires all moves to implement 3 functions:
        __init__(self)
        enact(self, context, attackerLoc, targetLocs)
        select(self, context, attackerLoc)

    init defines move's stats, enact executes the move, and select selects the targets of the move.
    
    Note: This is an abstract class and should not be instantiated.
    """
    @abstractmethod
    def __init__(self):
        """Defines characteristics of the move."""
        pass
    @abstractmethod
    def enact(self, context, attackerLoc, targetLocs):
        """Executes the move using the battle context from attacker location to target locations.
        
        Arguments:
            context (dict): Battle context.
            attackerLoc (BattleLocation): BattleLocation of the attacker.
            targetLocs (list): List of BattleLocation's of the targets.
        """
        pass
    @abstractmethod
    def select(self, context, attackerLoc):
        """Selects targets and returns a list of the target's BattleLocations.

        Arguments:
            context (dict): Battle context.
            attackerLoc (BattleLocation): BattleLocation of the attacker.
        
        Returns:
            list: List of the BattleLocations of each target selected.
        """
        pass

class Tackle(Move):
    """Tackle move

    This class encompasses all information, behavior, and targeting for the move, Tackle.

    Attributes:
        N/A
    """
    def __init__(self):
        self.power=20
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.NORMAL
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLocLoc):
        return SelectSingleTarget.select(context, attackerLocLoc)

class Earthquake(Move):
    """Earthquake move
    
    This class encompasses all information, behavior, and targeting for the move, Earthquake

    Attributes:
        N/A
    """
    def __init__(self):
        self.power=100
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.GROUND
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)

class Thunder(Move):
    """Thunder move
    
    This class encompasses all information, behavior, and targeting for the move, Thunder

    Attributes:
        N/A
    """
    def __init__(self):
        self.power=120
        self.accuracy=0.7
        self.critChance=CRITCHANCE
        self.isPhys=False
        self.type=Type.ELECTRIC
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    def enact(self, context, attackerLoc, targetLocs):
        AttackSingleTarget.do(context, self, attackerLoc, targetLocs)
    def select(self, context, attackerLocLoc):
        return SelectSingleTarget.select(context, attackerLocLoc)