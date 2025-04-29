from abc import ABC, abstractmethod
from globals import *
class Move(ABC):
    """Abstract class for moves.

    This is an abstract class that requires all moves to implement 3 functions:
        __init__(self)
        enact(self, battleContext, attackerLoc, defenderLocs)
        select(self, battleContext, attackerLoc)

    init defines move's stats, enact executes the move, and select selects the targets of the move.
    
    Note: This is an abstract class and should not be instantiated.
    """
    @abstractmethod
    def __init__(self):
        """Defines characteristics of the move."""
        pass
    @abstractmethod
    def enact(self, battleContext):
        """Executes the move using the battle context from attacker location to target locations.
        
        Arguments:
            battleContext (BattleContext): Battle context.
        """
        pass
    @abstractmethod
    def select(self, battleContext, **kwargs):
        """Selects targets and returns a list of the target's BattleLocations.

        Arguments:
            battleContext (BattleContext): Battle context.
            attackerLoc (BattleLocation): BattleLocation of the attacker.
        
        Returns:
            list: List of the BattleLocations of each target selected.
        """
        pass