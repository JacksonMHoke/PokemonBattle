from dataclasses import dataclass
from gui import *

@dataclass
class EventContext:
    def __init__(self):
        self.cancelMove=False
        self.item=None
        self.attackMult=1

# Change this so that we have getters and setters for attacker, defender, etc but have them link up with
# movecontext intead that way we don't have to reference move context directly
@dataclass
class MoveEventContext:
    def __init__(self, moveContext, **kwargs):
        self.attackerLoc=moveContext.attackerLoc
        self.attacker=moveContext.attacker
        self.defenderLoc=moveContext.currentDefenderLoc
        self.defenderLocs=moveContext.defenderLocs
        self.move=moveContext.move
        self.moveContext=moveContext
        for k, v in kwargs.items():
            setattr(self, k, v)

@dataclass
class SelectActionEventContext:
    def __init__(self, pokemon, **kwargs):
        self.pokemon=pokemon
        self.trainer=self.pokemon.trainer
        self.team=self.trainer.team
        self.moves=self.pokemon.moves
        self.moveOptions=[DropdownItem(move.name, i) for i, move in enumerate(self.moves)]
        self.swapOptions=[DropdownItem(f'{t.name}: {p.name}', (t, p)) for t in self.team.trainers for p in self.trainer.getBenchedPokemon()]
        for k, v in kwargs.items():
            setattr(self, k, v)

@dataclass
class SwapEventContext:
    def __init__(self, oldPokemon, newPokemon, **kwargs):
        self.oldPokemon=oldPokemon
        self.newPokemon=newPokemon
        for k, v in kwargs.items():
            setattr(self, k, v)