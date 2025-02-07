from globals import *
from abc import ABC, abstractmethod
from random import random

class Action(ABC):
    @staticmethod
    @abstractmethod
    def do(self, context, move, currTrainer):
        pass

class singleTargetAttack(Action):
    def do(self, context, move, currTrainer):
        attPokemon=context[f'trainer{currTrainer}'].activePokemon
        defPokemon=context[f'trainer{1-currTrainer}'].activePokemon

        stab=STAB if move.type in attPokemon.typing else 1
        eff=1
        for t in defPokemon.typing:
            eff*=getEffectiveness(move.type, t)
        if random()<move.accuracy:
            dmg=(attPokemon.att/100)*move.power*stab*eff
            if random()<move.critChance:
                print('A critical hit!')
                dmg*=CRIT
            defPokemon.takeDamage(dmg, move.isPhys)
        else:
            print(move.name, 'missed!')

        context['trainer1'].updateActivePokemon()
        context['trainer2'].updateActivePokemon()