from behaviors.behaviors import SelectionBehavior
from gui import DropdownItem, showDropdown, waitForSubmit, hideDropdown
from random import random
from battle.battleaction import *

class SelectSingleTarget(SelectionBehavior):
    """Implements selection behavior for single target selection.

    This class provides the logic for selecting a single target on the battlefield
    from any team except user itself.

    Note: This class is used as a namespace for a static method `select` and is not intended to be instantiated
    """
    def select(context, **kwargs):
        """Returns list of a single target that is selected from user input.

        Arguments:
            context (Context): The battle context
        Keyword Arguments:
            attackerLoc (BattleLocation): Location of attacker

        Returns:
            list: List that consists of the BattleLocation of the target selected.  
        """
        attackerLoc=kwargs['attackerLoc']
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

        showDropdown(context=context, team=context.currentTeam, text='Select a target:', values=targetNames)
        v=waitForSubmit(context, context.currentTeam)
        hideDropdown(context=context, team=context.currentTeam)

        loc=validTargets[v[f'team{context.currentTeam+1}DDChoice'].id]
        if loc[1]==-1:
            return SelectSingleTarget.select(context, attackerLoc)
        return [context.teams[loc[0]].slots[loc[1]]]
    
class SelectSelf(SelectionBehavior):
    """Implements selection behavior for self targetting selection.

    This class contains logic for selecting self in target selection.

    Note: This class is used as a namespace for a static method `select` and should not be instantiated.
    """
    def select(context, **kwargs):
        """Selects self and returns loc
        
        Arguments:
            context (Context): The battle context
        Keyword Arguments:
            attackerLoc (BattleLocation): Location of attacker

        Returns:
            list: List that consists of the BattleLocation of self.  
        """
        return [kwargs['attackerLoc']]
    
class SelectNoTarget(SelectionBehavior):
    """Implements selection behavior for selecting no target.

    Note: This class is used as a namspace for a static method `select` and should not be instantiated.

    Returns:
            list: Empty list
    """
    def select(context, **kwargs):
        return []