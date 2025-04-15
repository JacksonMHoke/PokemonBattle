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
    def do(context):
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
    def do(context):
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
        attackMult=attacker.stats[Stat.ATT]/defender.stats[Stat.DEF] if move.isPhys else attacker.stats[Stat.SPA]/defender.stats[Stat.SPD]
        eff=1
        for t in defender.typing:
            eff*=getEffectiveness(move.type, t)

        if random()>move.accuracy:                  # TODO: Add evasiveness as a stat for miss calculation
            print(move.name, 'missed!', flush=True)
            context.window['combatLog'].update(f'{move.name} missed!\n', append=True)
            return
        
        if eff>1:
            print(f'{move.name} was super effective!', flush=True)
            context.window['combatLog'].update(f'{move.name} was super effective!\n', append=True)
        elif eff<1:
            print(f'{move.name} was ineffective...', flush=True)
            context.window['combatLog'].update(f'{move.name} was ineffective!\n', append=True)

        dmg=attackMult*move.power*stab*eff
        if random()<move.critChance:
            print('A critical hit!', flush=True)
            context.window['combatLog'].update(f'A critical hit!\n', append=True)
            dmg*=CRIT

        defender.takeDamage(dmg, context)

'''
Buffing Behavior
'''

'''
Misc Behavior
'''

class StatusSingleTarget(ExecutionBehavior):
    """Implements execution behavior for a single target status

    This class implements statusing a single pokemon.

    Note:
        This class is used as a namespace for a static method `do` and is not intended to be instantiated
    """
    def do(context):
        """Statuses target with a status

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
        defender.status=context.inflictedStatus

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
    from any team except user itself.

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
        validTargets=[]
        targetNames=[]
        for i, team in enumerate(context.teams):
            targetNames.append(DropdownItem(f'--{team.teamName}--', len(targetNames)))
            validTargets.append((i, -1))
            for j, slot in enumerate(team.slots):
                if slot.pokemon is None or slot.pokemon.name==attacker.name and attackerLoc.teamIdx==i:
                    continue
                else:
                    targetNames.append(DropdownItem(slot.pokemon.name, len(targetNames)))
                    validTargets.append((i, j))
        if len(validTargets)==len(context.teams):
            raise Exception('No targets found!')
        if len(validTargets)==len(context.teams)+1:
            loc=[l for l in validTargets if l[1]!=-1][0]
            return [context.teams[loc[0]].slots[loc[1]]]

        context.window[f'team{context.currentTeam+1}DDTitle'].update(value='Select a target:')
        context.window[f'team{context.currentTeam+1}DD'].update(visible=True)
        context.window[f'team{context.currentTeam+1}DDChoice'].update(values=targetNames)
        context.window.refresh()
        v=waitForSubmit(context)
        context.window[f'team{context.currentTeam+1}DD'].update(visible=False)
        loc=validTargets[v[f'team{context.currentTeam+1}DDChoice'].id]
        if loc[1]==-1:
            return SelectSingleTarget.select(context, attackerLoc)
        return [context.teams[loc[0]].slots[loc[1]]]