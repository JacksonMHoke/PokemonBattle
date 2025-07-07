from globals import *
class StatBuff:
    """Stat buff class. Calculation is done through (base+flat)*(1.0+mult)

    Attributes:
        name (str): Name of buff
        flat (int): Flat stat buff amount
        mult (float): Mult stat buff amount
        id (int): Unique ID
    """
    def __init__(self, name=None, flat=0, mult=0):
        self.name=name
        self.flat=flat
        self.mult=mult
        self.id=getUniqueID()

    def isActive(self, currentTurn):
        """Returns true if buff should be applied this turn."""
        return True
    
    def isExpired(self, currentTurn):
        """Returns true if buff has expired"""
        return False

class TimedStatBuff(StatBuff):
    """Timed stat buff class. Same as StatBuff class but has a start turn and duration.

    Attributes:
        startTurn (int): Turn to start buffing stat
        duration (int): Number of turns for buff to last
    """
    def __init__(self, startTurn, duration, name=None, flat=0, mult=0):
        super().__init__(name=name, flat=flat, mult=mult)
        self.startTurn=startTurn
        self.duration=duration

    def isActive(self, currentTurn):
        return self.startTurn<=currentTurn<self.startTurn+self.duration
    
    def isExpired(self, currentTurn):
        return self.startTurn+self.duration<=currentTurn