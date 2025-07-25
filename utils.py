from globals import *

def matchById(obj):
    return lambda x: x.id==obj.id

def isValidTargeting(moveContext):
    """Takes move context and returns true if targeting is valid"""
    if moveContext.attacker and moveContext.attacker.state==State.ACTIVE and moveContext.defender:
        return True
    return False

class Damage:
    def __init__(self, basePower, attackMult=1, stab=1, effectiveness=1, crit=1, additionalMult=1, flatBonus=0):
        self.basePower=basePower
        self.attackMult=attackMult
        self.stab=stab
        self.effectiveness=effectiveness
        self.crit=crit
        self.flatBonus=flatBonus
        self.damageCap=float('inf')
    
    def total(self, attackDefRatio):
        return min(self.basePower*attackDefRatio*self.attackMult*self.stab*self.effectiveness*self.crit+self.flatBonus, self.damageCap)
    
    def __repr__(self):
        return str(self.total)