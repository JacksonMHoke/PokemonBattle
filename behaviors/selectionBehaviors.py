from behaviors.behaviors import SelectionBehavior
from gui import DropdownItem, showDropdown, waitForSubmit, hideDropdown
from random import random
from battle.battleAction import *

class SelectSingleTarget(SelectionBehavior):
    """Implements selection behavior for single target selection.

    This class provides the logic for selecting a single target on the battlefield
    from any team except user itself.

    Note: This class is used as a namespace for a static method `select` and is not intended to be instantiated
    """
    def select(battleContext, eventContext, **kwargs):
        """Returns list of a single target that is selected from user input.

        Arguments:
            battleContext (BattleContext): The battle context
        Keyword Arguments:
            attackerLoc (BattleLocation): Location of attacker

        Returns:
            list: List that consists of the BattleLocation of the target selected.  
        """
        attackerLoc=kwargs['attackerLoc']
        attacker=attackerLoc.pokemon
        validTargets=[]
        targetNames=[]
        for i, team in enumerate(battleContext.teams):
            targetNames.append(DropdownItem(f'--{team.teamName}--', len(targetNames)))
            validTargets.append((i, -1))
            for j, slot in enumerate(team.slots):
                if slot.pokemon is None or slot.pokemon.name==attacker.name and attackerLoc.teamIdx==i:
                    continue
                else:
                    targetNames.append(DropdownItem(slot.pokemon.name, len(targetNames)))
                    validTargets.append((i, j))
        if len(validTargets)==len(battleContext.teams):
            raise Exception('No targets found!')
        if len(validTargets)==len(battleContext.teams)+1:
            loc=[l for l in validTargets if l[1]!=-1][0]
            return [battleContext.teams[loc[0]].slots[loc[1]]]

        showDropdown(battleContext=battleContext, team=battleContext.currentTeam, text='Select a target:', values=targetNames)
        v=waitForSubmit(battleContext, battleContext.currentTeam)
        hideDropdown(battleContext=battleContext, team=battleContext.currentTeam)

        loc=validTargets[v[f'team{battleContext.currentTeam+1}DDChoice'].id]
        if loc[1]==-1:
            return SelectSingleTarget.select(battleContext, attackerLoc)
        return [battleContext.teams[loc[0]].slots[loc[1]]]
    
class SelectSelf(SelectionBehavior):
    """Implements selection behavior for self targetting selection.

    This class contains logic for selecting self in target selection.

    Note: This class is used as a namespace for a static method `select` and should not be instantiated.
    """
    def select(battleContext, eventContext, **kwargs):
        """Selects self and returns loc
        
        Arguments:
            battleContext (BattleContext): The battle context
        Keyword Arguments:
            attackerLoc (BattleLocation): Location of attacker

        Returns:
            list: List that consists of the BattleLocation of self.  
        """
        return [kwargs['attackerLoc']]
    
class SelectNoTarget(SelectionBehavior):
    """Implements selection behavior for selecting no target.

    Note: This class is used as a namspace for a static method `select` and should not be instantiated.

    Arguments:
        battleContext (BattleContext): The battle context

    Returns:
            list: Empty list
    """
    def select(battleContext, eventContext, **kwargs):
        return []