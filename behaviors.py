from globals import *
from abc import ABC, abstractmethod
from random import random
from battleaction import *

class ExecutionBehavior(ABC):
    """Abstract class for move behavior

    This class is an abstract class that requires a single function, do, that executes the desired
    behavior from the attacker to the targets.

    Note: This class is an abstract class and is not to be instantiated
    """
    @staticmethod
    @abstractmethod
    def do(context, move, attackerLoc, targetReqs):
        pass

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
    def do(context, move, attackerLoc, targetLocs):
        """Executes a single target attack.

        Arguments:
            context (Context): The battle context.
            move (Move): The move being used.
            attackerLoc (BattleLocation): Battle location of the attacker.
            targetLocs (list): List of BattleLocation's of the targets.
        
        Raises:
            AssertionError: If `targetLocs` does not contain exactly 1 target.
        """
        assert(len(targetLocs)==1)
        target=targetLocs[0].pokemon
        attacker=attackerLoc.pokemon

        # calc mults
        stab=STAB if move.type in attacker.typing else 1
        attackMult=attacker.stats[Stat.ATT]/target.stats[Stat.DEF] if move.isPhys else attacker.stats[Stat.SPA]/target.stats[Stat.SPD]
        eff=1
        for t in target.typing:
            eff*=getEffectiveness(move.type, t)

        if random()>move.accuracy:
            print(move.name, 'missed!', flush=True)
            return
        
        if eff>1:
            print(f'{move.name} was super effective!', flush=True)
        elif eff<1:
            print(f'{move.name} was ineffective...', flush=True)

        dmg=attackMult*move.power*stab*eff
        if random()<move.critChance:
            print('A critical hit!', flush=True)
            dmg*=CRIT

        target.takeDamage(dmg)

        # TODO: update all slots

'''
Buffing Behavior
'''

'''
Misc Behavior
'''

'''
Selection Behavior
'''

class SelectionBehavior(ABC):
    """Abstract class for selection behavior.

    This class is an abstract class that requires a single function, `select`, that takes in the attacker location and returns
    a list of target locations that are selected from user input. 

    Note:
        This class is an abstract class and is not to be instantiated
    """
    @staticmethod
    @abstractmethod
    def select(context, attackerLoc):
        pass

class SelectSingleTarget(SelectionBehavior):
    """Implements selection behavior for single target selection.

    This class provides the logic for selecting a single target on the battlefield
    from any team.

    Note: This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def select(context, attackerLoc):
        """Returns list of a single target that is selected from user input.

        Arguments:
            context (Context): The battle context
            attackerLoc (BattleLocation): The attacker's location in the battle

        Returns:
            list: List that consists of the BattleLocation of the target selected.  
        """
        attacker=attackerLoc.pokemon
        print(f'Team {context.teams[attackerLoc.teamIdx].teamName}\'s Pokemon {attacker.name} is choosing a target!', flush=True)
        for i, team in enumerate(context.teams):
            print(f'{i} Pokemon from Team {context.teams[i].teamName}:', flush=True)
            for j, slot in enumerate(team.slots):
                if slot.pokemon is None:
                    print('Empty')
                else:
                    print(j, slot.pokemon.name, flush=True)
        try:
            targetTeam=int(input('Select team to target by number: '))
            targetTeam=clamp(targetTeam, 0, len(context.teams)-1)
            print(f'Team {context.teams[targetTeam].teamName} was selected as a target!', flush=True)
            targetMon=int(input('Select pokemon to target by number: '))
            targetMon=clamp(targetMon, 0, len(context.teams[targetTeam].slots)-1)
            print(f'{context.teams[targetTeam].slots[targetMon].pokemon.name} was selected as a target!\n\n', flush=True)
        except:
            return SelectSingleTarget.select(context, attackerLoc)
        
        return [context.teams[targetTeam].slots[targetMon]]