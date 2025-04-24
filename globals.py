from enum import Enum, IntEnum

"""
This file contains all ENUMs, helper functions, and also constants.

Multipliers:
STAB, CRIT, CRITCHANCE

ENUMs:
Stat, Type, Prio, State

Helper Functions:
get_effectiveness(attackingType, defendingType)
clamp(n, smallest, largest)
"""

STAB=1.5
CRIT=1.5
CRITCHANCE=0.1
MINMULT=0
MAXMULT=4

class Type(Enum):
    NORMAL=1
    FIGHTING=2
    FIRE=3
    WATER=4
    GRASS=5
    ELECTRIC=6
    ICE=7
    POISON=8
    GROUND=9
    FLYING=10
    PSYCHIC=11
    BUG=12
    ROCK=13
    GHOST=14
    DARK=15
    DRAGON=16
    STEEL=17
    FAIRY=18

class Prio(IntEnum):
    RUN=10000
    SWAP=9999
    ITEM=9998
    FASTMOVE=1
    MOVE=0

class State(Enum):
    FAINTED=0
    BENCHED=1
    ACTIVE=2

class Trigger(Enum):
    START=0
    EQUIP=1
    UNEQUIP=2
    BEFORE_MOVE=3
    AFTER_STATUS=4
    AFTER_MOVE=5
    END_TURN_STATUS=6

# Effectiveness multipliers:
# For any (attacker, defender) pair not listed, assume a multiplier of 1.
effectiveness = {
    Type.NORMAL: {
        Type.ROCK:   0.5,
        Type.GHOST:  0,
        Type.STEEL:  0.5,
    },
    Type.FIRE: {
        Type.FIRE:    0.5,
        Type.WATER:   0.5,
        Type.GRASS:   2,
        Type.ICE:     2,
        Type.BUG:     2,
        Type.ROCK:    0.5,
        Type.DRAGON:  0.5,
        Type.STEEL:   2,
    },
    Type.WATER: {
        Type.FIRE:    2,
        Type.WATER:   0.5,
        Type.GRASS:   0.5,
        Type.GROUND:  2,
        Type.ROCK:    2,
        Type.DRAGON:  0.5,
    },
    Type.ELECTRIC: {
        Type.WATER:   2,
        Type.ELECTRIC:0.5,
        Type.GRASS:   0.5,
        Type.GROUND:  0,    # No effect
        Type.FLYING:  2,
        Type.DRAGON:  0.5,
    },
    Type.GRASS: {
        Type.FIRE:    0.5,
        Type.WATER:   2,
        Type.GRASS:   0.5,
        Type.POISON:  0.5,
        Type.GROUND:  2,
        Type.FLYING:  0.5,
        Type.BUG:     0.5,
        Type.ROCK:    2,
        Type.DRAGON:  0.5,
        Type.STEEL:   0.5,
    },
    Type.ICE: {
        Type.FIRE:    0.5,
        Type.WATER:   0.5,
        Type.GRASS:   2,
        Type.ICE:     0.5,
        Type.GROUND:  2,
        Type.FLYING:  2,
        Type.DRAGON:  2,
        Type.STEEL:   0.5,
    },
    Type.FIGHTING: {
        Type.NORMAL:  2,
        Type.ICE:     2,
        Type.POISON:  0.5,
        Type.FLYING:  0.5,
        Type.PSYCHIC: 0.5,
        Type.BUG:     0.5,
        Type.ROCK:    2,
        Type.GHOST:   0,
        Type.DARK:    2,
        Type.STEEL:   2,
        Type.FAIRY:   0.5,
    },
    Type.POISON: {
        Type.GRASS:   2,
        Type.POISON:  0.5,
        Type.GROUND:  0.5,
        Type.ROCK:    0.5,
        Type.GHOST:   0.5,
        Type.STEEL:   0,
        Type.FAIRY:   2,
    },
    Type.GROUND: {
        Type.FIRE:    2,
        Type.ELECTRIC:2,
        Type.GRASS:   0.5,
        Type.POISON:  2,
        Type.FLYING:  0,    # No effect
        Type.BUG:     0.5,
        Type.ROCK:    2,
        Type.STEEL:   2,
    },
    Type.FLYING: {
        Type.ELECTRIC:0.5,
        Type.GRASS:   2,
        Type.FIGHTING:2,
        Type.BUG:     2,
        Type.ROCK:    0.5,
        Type.STEEL:   0.5,
    },
    Type.PSYCHIC: {
        Type.FIGHTING:2,
        Type.POISON:  2,
        Type.PSYCHIC: 0.5,
        Type.STEEL:   0.5,
        Type.DARK:    0,    # No effect
    },
    Type.BUG: {
        Type.GRASS:   2,
        Type.FIRE:    0.5,
        Type.FIGHTING:0.5,
        Type.POISON:  0.5,
        Type.FLYING:  0.5,
        Type.PSYCHIC: 2,
        Type.GHOST:   0.5,
        Type.DARK:    2,
        Type.STEEL:   0.5,
        Type.FAIRY:   0.5,
    },
    Type.ROCK: {
        Type.FIRE:    2,
        Type.ICE:     2,
        Type.FIGHTING:0.5,
        Type.GROUND:  0.5,
        Type.FLYING:  2,
        Type.BUG:     2,
        Type.STEEL:   0.5,
    },
    Type.GHOST: {
        Type.NORMAL:  0,
        Type.PSYCHIC: 2,
        Type.GHOST:   2,
        Type.DARK:    0.5,
    },
    Type.DRAGON: {
        Type.DRAGON:  2,
        Type.STEEL:   0.5,
        Type.FAIRY:   0,    # No effect
    },
    Type.DARK: {
        Type.FIGHTING:0.5,
        Type.PSYCHIC: 2,
        Type.GHOST:   2,
        Type.DARK:    0.5,
        Type.FAIRY:   0.5,
    },
    Type.STEEL: {
        Type.FIRE:    0.5,
        Type.WATER:   0.5,
        Type.ELECTRIC:0.5,
        Type.ICE:     2,
        Type.ROCK:    2,
        Type.STEEL:   0.5,
        Type.FAIRY:   2,
    },
    Type.FAIRY: {
        Type.FIRE:    0.5,
        Type.FIGHTING:2,
        Type.POISON:  0.5,
        Type.DRAGON:  2,
        Type.DARK:    2,
        Type.STEEL:   0.5,
    },
}

# Example function to retrieve the multiplier with a default of 1:
def getEffectiveness(attackingType, defendingType):
    """Returns damage multiplier for attackingType attacking defendingType"""
    return effectiveness.get(attackingType, {}).get(defendingType, 1)

def clamp(n, smallest, largest):
    """Returns n clamped between smallest and largest inclusive"""
    return min(max(smallest, n), largest)