from abc import ABC, abstractmethod
from random import random
from globals import *
from gui import *
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
        super().__init__(turn, move.priority, attackerLoc.pokemon.stats[Stat.SPE])
        self.move=move
        self.attackerLoc=attackerLoc
        self.defenderLocs=defenderLocs
    def execute(self, context):
        """Executes the move using the context, attacker location, and target locations.

        Arguments:
            context (Context): Battle context
        """
        if self.attackerLoc.pokemonAtSelection.state!=State.ACTIVE:                                     # TODO: will have to change for moves like future sight
            return
        context.prepareMove(attackerLoc=self.attackerLoc, defenderLocs=self.defenderLocs, move=self.move)
        self.move.enact(context=context)
    
class BattleLocation:
    """Represents a slot or location on the battlefield.

    This class stores all the information needed to select actions from this location.

    Attributes:
        teamIdx (int): Team index.
        slotIdx (int): Slot index.
        trainer (Trainer): Trainer of pokemon at this location
        pokemonAtSelection (Pokemon): Pokemon at this location when action was selected
        pokemon (Pokemon): Pokemon at this location right now

    Note: pokemonAtSelection is mainly used for specific moves like Pursuit
    """
    def __init__(self, teamIdx, slotIdx, trainer, pokemon):
        self.teamIdx=teamIdx
        self.slotIdx=slotIdx
        self.trainer=trainer
        self.pokemonAtSelection=None
        self.pokemon=pokemon

    def selectAction(self, context):
        """Selects action for the trainer and pokemon at this slot.

        Arguments:
            context (Context): Battle context
        """
        if self.pokemon is None:
            raise Exception('Selecting action from empty slot!')

        self.pokemonAtSelection=self.pokemon
        validMoves=self.pokemon.moves
        moveNames=[DropdownItem(move.name, i) for i, move in enumerate(validMoves)]

        showDropdown(context=context, team=context.currentTeam, text='Select a move:', values=moveNames)
        v=waitForSubmit(context, context.currentTeam)
        hideDropdown(context=context, team=context.currentTeam)

        move=validMoves[v[f'team{context.currentTeam+1}DDChoice'].id]
        targetsLoc=move.select(context, self)
        action=MoveAction(context.turn, move, self, targetsLoc)
        return action
    
    def clear(self):
        """Clears the slot and handles pokemon states accordingly"""
        if self.pokemon is None:
            return
        assert self.pokemon.state!=State.BENCHED
        if self.pokemon.state==State.ACTIVE:
            self.pokemon.state=State.BENCHED

        self.pokemon=None
        self.trainer=None
    
    def swapPokemon(self, trainer, pokemon):
        """Swaps pokemon off this slot in place for a new pokemon and their trainer.

        Arguments:
            trainer (Trainer): Trainer of pokemon to be swapped in
            pokemon (Pokemon): Pokemon to be swapped in
        """
        assert pokemon.state==State.BENCHED

        self.clear()
        self.pokemon=pokemon
        self.pokemon.state=State.ACTIVE
        self.trainer=trainer