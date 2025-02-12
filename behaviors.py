from globals import *
from abc import ABC, abstractmethod
from random import random
from battleaction import *

class ExecutionBehavior(ABC):
    @staticmethod
    @abstractmethod
    def do(context, move, targetReqs):
        pass

'''
Attacking Behavior
'''
class AttackSingleTarget(ExecutionBehavior):
    def do(context, move, attackerLoc, targetLocs):
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
    @staticmethod
    @abstractmethod
    def select(context, attackerLoc):
        pass

class SelectSingleTarget(SelectionBehavior):
    def select(context, attackerLoc):
        attacker=attackerLoc.pokemon
        print(f'Team {context['teams'][attackerLoc.teamIdx].teamName}\'s Pokemon {attacker.name} is choosing a target!', flush=True)
        for i, team in enumerate(context['teams']):
            print(f'{i} Pokemon from Team {context['teams'][i].teamName}:', flush=True)
            for j, slot in enumerate(team.slots):
                if slot.pokemon is None:
                    print('Empty')
                else:
                    print(j, slot.pokemon.name, flush=True)
        try:
            targetTeam=int(input('Select team to target by number: '))
            targetTeam=clamp(targetTeam, 0, len(context['teams'])-1)
            print(f'Team {context['teams'][targetTeam].teamName} was selected as a target!', flush=True)
            targetMon=int(input('Select pokemon to target by number: '))
            targetMon=clamp(targetMon, 0, len(context['teams'][targetTeam].slots)-1)
            print(f'{context['teams'][targetTeam].slots[targetMon].pokemon.name} was selected as a target!\n\n', flush=True)
        except:
            return SelectSingleTarget.select(context, attackerLoc)
        
        
        return context['teams'][targetTeam].slots[targetMon]