from globals import *
from abc import ABC, abstractmethod
from random import random
from battleaction import *

class ExecutionBehavior(ABC):
    @staticmethod
    @abstractmethod
    def do(context, move, targetReqs):
        pass

class SelectionBehavior(ABC):
    @staticmethod
    @abstractmethod
    def select(context, attackerLoc):
        pass

'''
Attacking Behavior
'''
class AttackSingleTarget(ExecutionBehavior):
    def do(context, move, attacker, targetReqs):
        assert(len(targetReqs)==1)
        target=targetReqs[0].resolve(context)

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

        target.takeDamage(dmg, move.isPhys)

'''
Buffing Behavior
'''

'''
Misc Behavior
'''

class SelectSingleTarget(SelectionBehavior):
    def select(context, attackerLoc):
        attacker=attackerLoc.resolve(context)
        curr=0
        print(f'Team {context['teams'][attackerLoc.team].teamName}\'s Pokemon {attacker.name} is choosing a target!', flush=True)
        for i, team in enumerate(context['teams']):
            print(f'{i} Pokemon from Team {context['teams'][i].teamName}:', flush=True)
            for j, mon in enumerate(team.slots):
                print(j, mon.name, flush=True)
        try:
            targetTeam=int(input('Select team to target by number: '))
            targetMon=int(input('Select pokemon to target by number: '))
        except:
            return SelectSingleTarget.select(context, attackerLoc)
        targetTeam=clamp(targetTeam, 0, len(context['teams'])-1)
        targetMon=clamp(targetMon, 0, len(context['teams'][targetTeam].slots)-1)
        return [BattleLocation(targetTeam, targetMon, context['teams'][targetTeam][targetMon])]