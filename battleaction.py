from abc import ABC, abstractmethod
from random import random
from globals import *
class BattleAction(ABC):
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
    def __init__(self, turn, move, attackerLoc, targetLocs):
        super().__init__(turn, move.priority, attackerLoc.pokemon.stats[Stat.SPE])
        self.move=move
        self.attackerLoc=attackerLoc
        self.targetLocs=targetLocs
    def execute(self, context):
        self.move.enact(context, self.attackerLoc, self.targetLocs)
    
class BattleLocation:
    def __init__(self, teamIdx, slotIdx, trainer, pokemon):
        self.teamIdx=teamIdx
        self.slotIdx=slotIdx
        self.trainer=trainer
        self.pokemonAtSelection=None           # used for moves like pursuit that require information on what pokemon was there at move selection
        self.pokemon=pokemon

    def selectAction(self, context):
        self.pokemonAtSelection=self.pokemon
        validMoves=self.pokemon.moves
        print(f'{self.trainer.name} is picking a move for {self.pokemon.name}', flush=True)
        print('List of moves:', len(validMoves), flush=True)
        for i, move in enumerate(validMoves):
            print('\t', i, move.name, flush=True)
        try:
            choice=int(input('Select the move by number: '))
        except:
            return self.selectAction(context)
        selectedMove=validMoves[clamp(choice, 0, len(validMoves)-1)]
        print(f'{selectedMove.name} was selected.\n\n', flush=True)
        targetsLoc=selectedMove.select(context, self)
        action=MoveAction(context['turn'], selectedMove, self, targetsLoc)
        return action
    
    def swapPokemon(self, trainer, pokemon):
        self.pokemon=pokemon
        self.trainer=trainer