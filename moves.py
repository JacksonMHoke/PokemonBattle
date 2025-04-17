from abc import ABC, abstractmethod
from globals import *
from behaviors import *
from battleaction import *
from event import *
from decorators import *
class Move(ABC):
    """Abstract class for moves.

    This is an abstract class that requires all moves to implement 3 functions:
        __init__(self)
        enact(self, context, attackerLoc, defenderLocs)
        select(self, context, attackerLoc)

    init defines move's stats, enact executes the move, and select selects the targets of the move.
    
    Note: This is an abstract class and should not be instantiated.
    """
    @abstractmethod
    def __init__(self):
        """Defines characteristics of the move."""
        pass
    @abstractmethod
    def enact(self, context):
        """Executes the move using the battle context from attacker location to target locations.
        
        Arguments:
            context (Context): Battle context.
        """
        pass
    @abstractmethod
    def select(self, context, attackerLoc):
        """Selects targets and returns a list of the target's BattleLocations.

        Arguments:
            context (Context): Battle context.
            attackerLoc (BattleLocation): BattleLocation of the attacker.
        
        Returns:
            list: List of the BattleLocations of each target selected.
        """
        pass

class Tackle(Move):
    """Tackle move

    This class encompasses all information, behavior, and targeting for the move, Tackle.

    Attributes:
        power (int): Power of move
        accuracy (float): Accuracy of move between 0 and 1
        critChance (float): Critical hit chance of move between 0 and 1
        isPhys (bool): Determines whether move is physical or not
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.power=20
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.NORMAL
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context)
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)

class Earthquake(Move):
    """Earthquake move
    
    This class encompasses all information, behavior, and targeting for the move, Earthquake

    Attributes:
        power (int): Power of move
        accuracy (float): Accuracy of move between 0 and 1
        critChance (float): Critical hit chance of move between 0 and 1
        isPhys (bool): Determines whether move is physical or not
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.power=100
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.GROUND
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context)
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)

class Thunder(Move):
    """Thunder move
    
    This class encompasses all information, behavior, and targeting for the move, Thunder

    Attributes:
        power (int): Power of move
        accuracy (float): Accuracy of move between 0 and 1
        critChance (float): Critical hit chance of move between 0 and 1
        isPhys (bool): Determines whether move is physical or not
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.power=120
        self.accuracy=0.7
        self.critChance=CRITCHANCE
        self.isPhys=False
        self.type=Type.ELECTRIC
        self.priority=Prio.FASTMOVE
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context)
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)
    
class Burn(Move):
    """Burn move

    Burns target
    
    Attributes:
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.name=self.__class__.__name__
        self.priority=Prio.MOVE
        self.type=Type.FIRE
    @moveDecorator
    def enact(self, context):
        context.inflictedStatus=Burned()
        StatusSingleTarget.do(context)
        context.inflictedStatus=None
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)
    
class Freeze(Move):
    """Freeze move

    Freezes target

    Attributes:
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.name=self.__class__.__name__
        self.priority=Prio.MOVE
        self.type=Type.ICE
    @moveDecorator
    def enact(self, context):
        context.inflictedStatus=Frozen()
        StatusSingleTarget.do(context)
        context.inflictedStatus=None
    def select(self, context, attackerLoc):
        return SelectSingleTarget.select(context, attackerLoc)