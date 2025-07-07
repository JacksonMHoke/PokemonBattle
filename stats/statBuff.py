from globals import *
class StatBuff:
    def __init__(self, name=None, flat=0, mult=0):
        self.name=name
        self.flat=flat
        self.mult=mult
        self.id=getUniqueID()

    def isActive(self, currentTurn):
        return True
    
    def isExpired(self, currentTurn):
        return False

class TimedStatBuff(StatBuff):
    def __init__(self, startTurn, duration, name=None, flat=0, mult=0):
        super().__init__(name=name, flat=flat, mult=mult)
        self.startTurn=startTurn
        self.duration=duration

    def isActive(self, currentTurn):
        return self.startTurn<=currentTurn<self.startTurn+self.duration
    
    def isExpired(self, currentTurn):
        return self.startTurn+self.duration<=currentTurn