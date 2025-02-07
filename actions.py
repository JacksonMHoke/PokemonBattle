from globals import *
from abc import ABC, abstractmethod
from random import random

class Action(ABC):
    @staticmethod
    @abstractmethod
    def do(context, move, currTrainer):
        pass

class singleTargetAttack(Action):
    def do(context, move, currTrainer):
        attPokemon=context[f'trainer{currTrainer}'].activePokemon
        defPokemon=context[f'trainer{3-currTrainer}'].activePokemon

        stab=STAB if move.type in attPokemon.typing else 1
        strength=attPokemon.stats[Stat.ATT] if move.isPhys else attPokemon.stats[Stat.SPA]
        eff=1
        for t in defPokemon.typing:
            eff*=getEffectiveness(move.type, t)
        if random()<move.accuracy:
            if eff>1:
                print(f'{move.name} was super effective!', flush=True)
            elif eff<1:
                print(f'{move.name} was ineffective...', flush=True)
            dmg=(strength/100)*move.power*stab*eff
            if random()<move.critChance:
                print('A critical hit!', flush=True)
                dmg*=CRIT
            defPokemon.takeDamage(dmg, move.isPhys)
        else:
            print(move.name, 'missed!', flush=True)

        context['trainer1'].updateActivePokemon()
        context['trainer2'].updateActivePokemon()