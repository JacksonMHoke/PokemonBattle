from abc import ABC, abstractmethod
from random import random
from globals import *
from gui import *
from contexts.moveContext import *
from contexts.eventContext import *
class BattleAction(ABC):
    """Represents an action in battle.

    This class is a parent class to various different actions. The lowest action
    is calculated in this order: lowest turn, highest priority, highest speed, then random
    if the rest are equal. Each BattleAction has an execute function that does the action.

    Attributes:
        turn (int): turn number
        priority (int): priority value
        speed (int): speed value

    Note: This class is an abstract class and is not to be instantiated.
    """
    def __init__(self, turn, priority, speed):
        self.turn=turn
        self.priority=priority
        self.speed=speed
    
    def __lt__(self, other):
        if self.turn!=other.turn:
            return self.turn<other.turn
        if self.priority!=other.priority:
            return self.priority>other.priority
        if self.speed!=other.speed:
            return self.speed>other.speed
        return random()<0.5
    
class SwapAction(BattleAction):
    """Represents a swap action activated using the execute function

    Attributes:
        swapLocation (BattleLocation): BattleLocation of the pokemon to be swapped out
        swapInPokemon (Pokemon): Pokemon to be swapped in
        trainer (Trainer): Trainer of the pokemon to be swapped in
    """
    def __init__(self, turn, swapLocation, swapInPokemon, trainer):
        super().__init__(turn, Prio.SWAP, 0)
        self.swapLocation=swapLocation
        self.swapInPokemon=swapInPokemon
        self.trainer=trainer
    def execute(self, battleContext):
        """Executes the move using the battleContext

        Arguments:
            battleContext (BattleContext): Battle Context
        """
        if self.swapInPokemon.status==State.FAINTED:
            battleContext.window['combatLog'].update(f'Could not swap in {self.swapInPokemon.name} because it has already fainted!!\n', append=True)
            return
        self.swapLocation.swapPokemon(self.swapInPokemon)
    
class MoveAction(BattleAction):
    """Represents a move action activated using the execute function.

    Attributes:
        move (Move): Move to be used.
        attackerLoc (BattleLocation): BattleLocation of the attacker.
        defenderLocs (list): List of BattleLocation's of the targets.

    This class is a child of the BattleAction class and carries the information needed
    to execute the move from the attacker to the targets.
    """
    def __init__(self, turn, move, attackerLoc, defenderLocs):
        super().__init__(turn, move.priority, attackerLoc.pokemon.stats.effectiveSpe)
        self.move=move
        self.attackerLoc=attackerLoc
        self.defenderLocs=defenderLocs
    def execute(self, battleContext):
        """Executes the move using the battleContext, attacker location, and target locations.

        Arguments:
            battleContext (BattleContext): Battle Context
        """
        if self.attackerLoc.pokemonAtSelection.state!=State.ACTIVE:
            return
        # TODO: Remove attacker, defender, move, etc from battle context and remove need for this function call
        battleContext.prepareMove(attackerLoc=self.attackerLoc, defenderLocs=self.defenderLocs, move=self.move)
        self.move.enact(battleContext=battleContext, moveContext=MoveContext(attackerLoc=self.attackerLoc, defenderLocs=self.defenderLocs, move=self.move))
    
class BattleLocation:
    """Represents a slot or location on the battlefield.

    This class stores all the information needed to select actions from this location.

    Attributes:
        teamIdx (int): Team index.
        slotIdx (int): Slot index.
        trainer (Trainer): Trainer of pokemon at this location
        pokemonAtSelection (Pokemon): Pokemon at this location when action was selected
        pokemon (Pokemon): Pokemon at this location right now

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle

    Note: pokemonAtSelection is mainly used for specific moves like Pursuit
    """
    def __init__(self, teamIdx, slotIdx, pokemon=None):
        self.teamIdx=teamIdx
        self.slotIdx=slotIdx
        self.pokemonAtSelection=None
        self.pokemon=pokemon

    def selectAction(self):
        """Selects action for the trainer and pokemon at this slot."""
        if self.pokemon is None:
            raise Exception('Selecting action from empty slot!')

        self.pokemonAtSelection=self.pokemon
        selectActionContext=SelectActionEventContext(pokemon=self.pokemon)
        self.battleContext.eventSystem.trigger(eventContext=selectActionContext, trigger=Trigger.BEFORE_ACTION_SELECT)

        showDropdown(battleContext=self.battleContext, team=self.teamIdx, text='Select a move:', values=selectActionContext.moveOptions)
        showSwapDropdown(battleContext=self.battleContext, team=self.teamIdx, text='', values=selectActionContext.swapOptions)
        v=waitForSubmit(self.battleContext, self.teamIdx)
        hideDropdown(battleContext=self.battleContext, team=self.teamIdx)
        hideSwapDropdown(self.battleContext, self.teamIdx)
        
        action=None
        if v[f'team{self.teamIdx+1}DDChoice']!='':
            # TODO: Add event for move selection in here or in move selection behavior
            move=selectActionContext.moves[v[f'team{self.teamIdx+1}DDChoice'].id]
            targetsLoc=move.select(self.battleContext, attackerLoc=self)
            action=MoveAction(self.battleContext.turn, move, self, targetsLoc)
        if v[f'team{self.teamIdx+1}DDSwapChoice']!='':
            trainer, pokemon=v[f'team{self.teamIdx+1}DDSwapChoice'].id
            action=SwapAction(self.battleContext.turn, self, pokemon, trainer)
        return action
    
    def clear(self):
        """Clears the slot and handles pokemon states accordingly"""
        if self.pokemon is None:
            return
        assert self.pokemon.state!=State.BENCHED
        if self.pokemon.state==State.ACTIVE:
            self.pokemon.state=State.BENCHED

        self.pokemon=None
    
    # TODO: Separate between sending out pokemon and swapping a pokemon with another slot
    def swapPokemon(self, pokemon):
        """Swaps pokemon off this slot in place for a new pokemon and their trainer.

        Arguments:
            trainer (Trainer): Trainer of pokemon to be swapped in
            pokemon (Pokemon): Pokemon to be swapped in
        """
        assert pokemon.state==State.BENCHED

        swapContext = SwapEventContext(oldPokemon=self.pokemon, newPokemon=pokemon, cancelSwap=False)
        self.battleContext.eventSystem.trigger(eventContext=swapContext, trigger=Trigger.BEFORE_SWAP)
        if swapContext.cancelSwap:
            return

        if self.pokemon is None:
            self.battleContext.window['combatLog'].update(f'Sending out {pokemon.name}!\n', append=True)
        else:
            self.battleContext.window['combatLog'].update(f'Swapped {self.pokemon.name} and {pokemon.name}!\n', append=True)

        self.clear()
        self.pokemon=swapContext.newPokemon
        self.pokemon.state=State.ACTIVE

        self.battleContext.eventSystem.trigger(
            eventContext=SwapEventContext(oldPokemon=swapContext.oldPokemon, newPokemon=swapContext.newPokemon),
            trigger=Trigger.AFTER_SWAP
        )



    # Enforces that battleContext is set before used
    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext

    @battleContext.setter
    def battleContext(self, battleContext):
        """Sets battle context"""
        self._battleContext=battleContext

    @property
    def trainer(self):
        return self.pokemon.trainer if self.pokemon is not None else None