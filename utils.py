def matchById(obj):
    return lambda x: x.id==obj.id

class Damage:
    def __init__(self, basePower, attackMult=1, stab=1, effectiveness=1, crit=1, additionalMult=1, flatBonus=0):
        self.basePower=basePower
        self.attackMult=attackMult
        self.stab=stab
        self.effectiveness=effectiveness
        self.crit=crit
        self.additionalMult=additionalMult
        self.flatBonus=flatBonus
        self.damageCap=float('inf')
    
    @property
    def total(self):
        return min(self.basePower*self.attackMult*self.stab*self.effectiveness*self.crit*self.additionalMult+self.flatBonus, self.damageCap)
    
    def __repr__(self):
        return str(self.total)