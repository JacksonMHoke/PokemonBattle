from moves.move import Move
from behaviors.selectionBehaviors import *
from behaviors.executionBehaviors import *
from events.statuses import *
from events.weathers import *
from battle.battleaction import *
from decorators import *

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
        AttackSingleTarget.do(context=context)
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)

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
        AttackSingleTarget.do(context=context)
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)

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
        self.priority=Prio.MOVE
        self.paraChance=0.3
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context)
        if context.missedMove==False and random()<self.paraChance:
            StatusSingleTarget.do(context=context, inflictedStatus=Paralyzed())
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
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
        StatusSingleTarget.do(context=context, inflictedStatus=Burned())
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
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
        StatusSingleTarget.do(context=context, inflictedStatus=Frozen())
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
class ThunderWave(Move):
    """Thunder Wave move

    Paralyzes target

    Attributes:
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.name=self.__class__.__name__
        self.priority=Prio.MOVE
        self.type=Type.ELECTRIC
    @moveDecorator
    def enact(self, context):
        StatusSingleTarget.do(context=context, inflictedStatus=Paralyzed())
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
class Rest(Move):
    """Rest move
    
    Sleep and restore health to full.
    
    Attributes:
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.name=self.__class__.__name__
        self.priority=Prio.MOVE
        self.type=Type.NORMAL
        self.healPower=9999
    @moveDecorator
    def enact(self, context):
        StatusSelf.do(context=context, inflictedStatus=Asleep())
        HealSingleTarget.do(context=context)
    def select(self, context, **kwargs):
        return SelectSelf.select(context=context, **kwargs)
    
class RainDance(Move):
    """Rain Dance move

    Sets rain for 4 turns

    Attributes:
        type (Type): Type of move
        priority (Priority): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.name=self.__class__.__name__
        self.priority=Prio.MOVE
        self.type=Type.WATER
    @moveDecorator
    def enact(self, context):
        SetWeather.do(context=context, weatherToSet=Rain())
    def select(self, context, **kwargs):
        return SelectNoTarget.select(context=context, **kwargs)

class WaterLance(Move):
    """Water Lance move

    Deals low damage multiple times.

    Attributes:
        power (int): Power of move
        accuracy (float): Accuracy of move between 0 and 1
        critChance (float): Critical hit chance of move between 0 and 1
        isPhys (bool): Determines whether move is physical or not
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
        numHits (int): Number of times move hits
    """
    def __init__(self):
        self.power=25
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.WATER
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
        self.numHits=2
    @moveDecorator
    def enact(self, context):
        for i in range(self.numHits):
            AttackSingleTarget.do(context=context)
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
class SwordsDance(Move):
    """Swords Dance

    Buffs attack by 1 mult.
    
    Attributes:
        type (Type): Type of move
        priority (Prio): Priority of move
        name (str): Name of move
        statToBuff (str): Name of stat
        buffMult (float): Multiplier to add to stat multiplier
    """
    def __init__(self):
        self.type=Type.NORMAL
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
        self.statToBuff='ATT'
        self.buffMult=1.0
    @moveDecorator
    def enact(self, context):
        BuffSingleTarget.do(context=context, statToBuff=self.statToBuff, buffMult=self.buffMult)
    def select(self, context, **kwargs):
        return SelectSelf.select(context=context, **kwargs)
    
class FireBall(Move):
    """Fire Ball

    Deals damage to a single target, 10% chance to burn

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
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=False
        self.type=Type.FIRE
        self.priority=Prio.MOVE
        self.burnChance=0.1
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context=context)
        if context.missedMove==False and random()<self.burnChance:
            StatusSingleTarget.do(context=context, inflictedStatus=Burned())
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
class FireSwipe(Move):
    """Fire Swipe

    Deals damage to target and steals target's item
    
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
        self.power=60
        self.accuracy=1
        self.critChance=CRITCHANCE
        self.isPhys=True
        self.type=Type.FIRE
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        AttackSingleTarget.do(context=context)
        StealItem.do(context=context)
    def select(self, context, **kwargs):
        return SelectSingleTarget.select(context=context, **kwargs)
    
class Conflagration(Move):
    """Conflagration
    
    Sets magma storm weather on field for 4 turns
    
    Attributes:
        type (Type): Type of move
        priorty (Prio): Priority of move
        name (str): Name of move
    """
    def __init__(self):
        self.type=Type.FIRE
        self.priority=Prio.MOVE
        self.name=self.__class__.__name__
    @moveDecorator
    def enact(self, context):
        SetWeather.do(context=context, weatherToSet=MagmaStorm())
    def select(self, context, **kwargs):
        return SelectNoTarget.select(context=context, **kwargs)