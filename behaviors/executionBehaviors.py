from behaviors.behaviors import ExecutionBehavior
from random import random
from battle.battleAction import *
from globals import *
from contexts.battleContext import BattleContext
from contexts.eventContext import *
from decorators import executionBehaviorDecorator

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
    @executionBehaviorDecorator
    def do(battleContext, moveContext, eventContext, **kwargs):
        """Executes a single target attack.

        Arguments:
            battleContext (battleContext): The battle battleContext.
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=moveContext.defenderLocs
        attackerLoc=moveContext.attackerLoc
        attacker=moveContext.attacker
        move=moveContext.move

        assert(len(defenderLocs)==1)
        defenderLoc=defenderLocs[0]
        defender=defenderLocs[0].pokemon

        # calc mults
        stab=STAB if move.type in attacker.typing else 1
        attackMult=attacker.stats.effectiveAtt/defender.stats.effectiveDef if move.isPhys else attacker.stats.effectiveSpa/defender.stats.effectiveSpd
        eff=1
        for t in defender.typing:
            eff*=getEffectiveness(attackingType=move.type, defendingType=t)
        r=random()
        if r>move.accuracy:                  # TODO: Add evasiveness as a stat for miss calculation
            print(move.name, 'missed!', flush=True)
            battleContext.window['combatLog'].update(f'{move.name} missed!\n', append=True)
            return
        
        if eff>1:
            print(f'{move.name} was super effective!', flush=True)
            battleContext.window['combatLog'].update(f'{move.name} was super effective!\n', append=True)
        elif eff==0:
            print(f'{move.name} was ineffective...', flush=True)
            battleContext.window['combatLog'].update(f'{move.name} failed due to immunity...\n', append=True)
        elif eff<1:
            print(f'{move.name} was ineffective...', flush=True)
            battleContext.window['combatLog'].update(f'{move.name} was ineffective...\n', append=True)

        dmg=attackMult*move.power*stab*eff*eventContext.attackMult
        if random()<move.critChance:
            print('A critical hit!', flush=True)
            battleContext.window['combatLog'].update(f'A critical hit!\n', append=True)
            dmg*=CRIT

        defender.takeDamage(dmg=dmg)
        battleContext.eventSystem.trigger(
            eventContext=AfterHitEventContext(
                attackerLoc=attackerLoc,
                defenderLoc=defenderLoc,
                attacker=attacker,
                defender=defender,
                move=move,
                dmg=dmg),
            trigger=Trigger.AFTER_HIT)


'''
Buffing Behavior
'''

class BuffSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target buff

    This class provides the logic for executing a move that buffs a single target using information stored 
    in the battleContext object.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    @executionBehaviorDecorator
    def do(battleContext, eventContext, **kwargs):
        """Executes a single target buff.

        Arguments:
            battleContext (battleContext): The battle battleContext.
        Keyword Arguments:
            buff (StatBuff): Buff to apply to target
            stat (str): Stat to apply the buff to
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=battleContext.defenderLocs
        attackerLoc=battleContext.attackerLoc

        attacker=battleContext.attacker
        defenders=battleContext.defenders

        move=battleContext.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        defender.stats.addBuff(buff=kwargs['buff'], stat=kwargs['stat'])

class HealSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target heal

    This class provides the logic for executing a move that heals a single target. It heals based on the healing
    power of the move. Healing does not scale off of att/spa.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    @executionBehaviorDecorator
    def do(battleContext, eventContext, **kwargs):
        """Executes a single target heal.

        Arguments:
            battleContext (battleContext): The battle battleContext.

        Keyword Arguments:
            healAmount (int): Amount to heal target
        
        Raises:
            AssertionError: If `defenderLocs` does not contain exactly 1 target.
        """
        defenderLocs=battleContext.defenderLocs
        attackerLoc=battleContext.attackerLoc

        attacker=battleContext.attacker
        defenders=battleContext.defenders

        move=battleContext.move

        assert(len(defenderLocs)==1 and len(defenders)==1)

        defender=defenders[0]
        defender.heal(kwargs['healAmount'])

'''
Misc Behavior
'''
# class StealItem(ExecutionBehavior):
#     """Implements execution behavior for stealing defender's item.

#     This class provides logic and implementation for executing a move that steals the defender's item
#     """
#     def do(battleContext, eventContext, **kwargs):
#         """Steals target's item
        
#         Arguments:
#             battleContext (battleContext): The battle battleContext
#         """
#         defenderLocs=battleContext.defenderLocs
#         attackerLoc=battleContext.attackerLoc

#         attacker=battleContext.attacker
#         defenders=battleContext.defenders

#         move=battleContext.move

#         assert(len(defenderLocs)==1 and len(defenders)==1)

#         defender=defenders[0]
#         if attacker.item is not None or defender.item is None:
#             return
#         battleContext.window['combatLog'].update(f'{attacker.name} has stolen {defender.name}\'s {defender.item.name} item!\n', append=True)

#         eventContext.item=defender.item
#         battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.UNEQUIP)


#         attacker.item=defender.item
#         attacker.item.owner=attacker
#         defender.item=None
#         battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.EQUIP)



# class SetWeather(ExecutionBehavior):
#     """Implements execution behavior for setting weather effect.

#     This class provides logic and implementation for executing a move that sets or overrides a weather effect on the field.
#     Weather effect set is passed in through battleContext object in battleContext.setWeather
#     """
#     def do(battleContext, eventContext, **kwargs):
#         """Executes set weather

#         Arguments:
#             battleContext (battleContext): The battle battleContext
#         Keyword Arguements:
#             weatherToSet (Weather): Weather effect to set
#         """
#         weatherToSet=kwargs['weatherToSet']
#         if battleContext.weather is not None and battleContext.weather.name!=weatherToSet.name:
#             battleContext.window['combatLog'].update(f'{battleContext.weather.name} was replaced with {weatherToSet.name}\n', append=True)
#         elif battleContext.weather is not None:
#             battleContext.window['combatLog'].update(f'{battleContext.weather.name} is already active!\n', append=True)
#             return
#         else:
#             battleContext.window['combatLog'].update(f'{weatherToSet.name} is set!\n', append=True)
#         battleContext.weather=weatherToSet

# class StatusSingleTarget(ExecutionBehavior):
#     """Implements execution behavior for a single target status

#     This class implements statusing a single pokemon.

#     Note:
#         This class is used as a namespace for a static method `do` and is not intended to be instantiated
#     """
#     def do(battleContext, eventContext, **kwargs):
#         """Statuses target with a status

#         Arguments:
#             battleContext (battleContext): The battle battleContext.
#         Keyword Arguments:
#             inflictedStatus (Status): Status being inflicted onto defender
        
#         Raises:
#             AssertionError: If `defenderLocs` does not contain exactly 1 target.
#         """
#         defenderLocs=battleContext.defenderLocs
#         attackerLoc=battleContext.attackerLoc

#         attacker=battleContext.attacker
#         defenders=battleContext.defenders

#         move=battleContext.move

#         assert(len(defenderLocs)==1 and len(defenders)==1)

#         defender=defenders[0]
#         if defender.status is not None:
#             return
#         defender.status=kwargs['inflictedStatus']
#         kwargs['inflictedStatus'].owner=defender
#         scheduleEventAllTriggers(battleContext=battleContext, event=kwargs['inflictedStatus'])
#         battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.AFTER_STATUS)

# class StatusSelf(ExecutionBehavior):
#     """Implements execution behavior for statusing self
    
#     This class implements a statusing self behavior.
    
#     Arguments:
#         battleContext (battleContext): The battle battleContext
#     Keyword Arguments:
#         inflictedStatus (Status): Status to inflict on self
#     """
#     def do(battleContext, eventContext, **kwargs):
#         """
#         Statuses self

#         Arguments:
#             battleContext (battleContext): Battle battleContext
#         Keyword Arguments:
#             inflictedStatus (Status): Status to inflict
#         """
#         if battleContext.attacker.status is not None:
#             return
#         battleContext.attacker.status=kwargs['inflictedStatus']
#         kwargs['inflictedStatus'].owner=battleContext.attacker
#         scheduleEventAllTriggers(battleContext=battleContext, event=kwargs['inflictedStatus'])
#         battleContext.eventQueue.trigger(battleContext=battleContext, eventContext=eventContext, trigger=Trigger.AFTER_STATUS)