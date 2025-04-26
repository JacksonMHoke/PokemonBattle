from behaviors.behaviors import ExecutionBehavior
from random import random
from battle.battleaction import *

'''
Attacking Behavior
'''
class AttackSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target attack

    This class provides the logic for executing a move that targets a single target. It calculates
    various multipliers including stab bonuses, ATT/SPA to DEF/SPD ratios, type effectiveness, and critical hits.
    It also handles accuracy and prints messages to update what has occured.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def do(context, **kwargs):
        """Executes a single target attack.

        Arguments:
            context (Context): The battle context.
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=context.defenderLocs
        attackerLoc=context.attackerLoc

        attacker=context.attacker
        defenders=context.defenders

        move=context.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]

        # calc mults
        stab=STAB if move.type in attacker.typing else 1
        attackMult=attacker.stats.ATT/defender.stats.DEF if move.isPhys else attacker.stats.SPA/defender.stats.SPD
        eff=1
        for t in defender.typing:
            eff*=getEffectiveness(attackingType=move.type, defendingType=t)
        r=random()
        if r>move.accuracy:                  # TODO: Add evasiveness as a stat for miss calculation
            print(move.name, 'missed!', flush=True)
            context.window['combatLog'].update(f'{move.name} missed!\n', append=True)
            context.missedMove=True
            return
        context.missedMove=False
        
        if eff>1:
            print(f'{move.name} was super effective!', flush=True)
            context.window['combatLog'].update(f'{move.name} was super effective!\n', append=True)
        elif eff<1:
            print(f'{move.name} was ineffective...', flush=True)
            context.window['combatLog'].update(f'{move.name} was ineffective...\n', append=True)

        dmg=attackMult*move.power*stab*eff*context.attackMult
        if random()<move.critChance:
            print('A critical hit!', flush=True)
            context.window['combatLog'].update(f'A critical hit!\n', append=True)
            dmg*=CRIT

        defender.takeDamage(dmg=dmg, context=context)

'''
Buffing Behavior
'''

class BuffSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target buff

    This class provides the logic for executing a move that buffs a single target using information stored 
    in the context object.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def do(context, **kwargs):
        """Executes a single target buff.

        Arguments:
            context (Context): The battle context.
        Keyword Arguments:
            buffMult (float): Multiplier to add to stat
            statToBuff (str): String representation for stat (ex: 'HP' or 'ATT')
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=context.defenderLocs
        attackerLoc=context.attackerLoc

        attacker=context.attacker
        defenders=context.defenders

        move=context.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        defender.buffStatMult(stat=kwargs['statToBuff'], amount=kwargs['buffMult'], context=context)

class HealSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target heal

    This class provides the logic for executing a move that heals a single target. It heals based on the healing
    power of the move. Healing does not scale off of att/spa.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def do(context, **kwargs):
        """Executes a single target heal.

        Arguments:
            context (Context): The battle context.
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=context.defenderLocs
        attackerLoc=context.attackerLoc

        attacker=context.attacker
        defenders=context.defenders

        move=context.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        defender.heal(move.healPower, context)

'''
Misc Behavior
'''
class StealItem(ExecutionBehavior):
    """Implements execution behavior for stealing defender's item.

    This class provides logic and implementation for executing a move that steals the defender's item
    """
    def do(context, **kwargs):
        """Steals target's item
        
        Arguments:
            context (Context): The battle context
        """
        defenderLocs=context.defenderLocs
        attackerLoc=context.attackerLoc

        attacker=context.attacker
        defenders=context.defenders

        move=context.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        if attacker.item is not None or defender.item is None:
            return
        context.window['combatLog'].update(f'{attacker.name} has stolen {defender.name}\'s {defender.item.name} item!\n', append=True)

        context.triggerItem=attacker.item                               # TODO: SCUFFED CONTEXT
        context.triggerPokemon=defender                                 # TODO: SCUFFED CONTEXT
        triggerAllEvents(context, Trigger.UNEQUIP)


        attacker.item=defender.item
        defender.item=None
        context.triggerPokemon=attacker                                 # TODO: SCUFFED CONTEXT
        triggerAllEvents(context, Trigger.EQUIP)



class SetWeather(ExecutionBehavior):
    """Implements execution behavior for setting weather effect.

    This class provides logic and implementation for executing a move that sets or overrides a weather effect on the field.
    Weather effect set is passed in through context object in context.setWeather
    """
    def do(context, **kwargs):
        """Executes set weather

        Arguments:
            context (Context): The battle context
        Keyword Arguements:
            weatherToSet (Weather): Weather effect to set
        """
        weatherToSet=kwargs['weatherToSet']
        if context.weather is not None and context.weather.name!=weatherToSet.name:
            context.window['combatLog'].update(f'{context.weather.name} was replaced with {weatherToSet.name}\n', append=True)
        elif context.weather is not None:
            context.window['combatLog'].update(f'{context.weather.name} is already active!\n', append=True)
            return
        else:
            context.window['combatLog'].update(f'{weatherToSet.name} is set!\n', append=True)
        context.weather=weatherToSet

class StatusSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target status

    This class implements statusing a single pokemon.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def do(context, **kwargs):
        """Statuses target with a status

        Arguments:
            context (Context): The battle context.
        Keyword Arguments:
            inflictedStatus (Status): Status being inflicted onto defender
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=context.defenderLocs
        attackerLoc=context.attackerLoc

        attacker=context.attacker
        defenders=context.defenders

        move=context.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        if defender.status is not None:
            return
        defender.status=kwargs['inflictedStatus']
        context.inflictedPokemon=defender                           # TODO: SCUFFED CONTEXT

        triggerAllEvents(context, Trigger.AFTER_STATUS)

class StatusSelf(ExecutionBehavior):
    """Implements execution behavior for statusing self
    
    This class implements a statusing self behavior.
    
    Arguments:
        context (Context): The battle context
    Keyword Arguments:
        inflictedStatus (Status): Status to inflict on self
    """
    def do(context, **kwargs):
        """
        Statuses self with status stored in context.inflictedStatus
        """
        if context.attacker.status is not None:
            return
        context.attacker.status=kwargs['inflictedStatus']
        context.inflictedPokemon=context.attacker               # TODO: SCUFFED CONTEXT

        triggerAllEvents(context, Trigger.AFTER_STATUS)