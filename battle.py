from trainer import *
from pokemon import *
from moves import *
from battlequeue import *
from tabulate import tabulate
from random import random

class Battle:
    def __init__(self, teams):
        self.context={}
        self.context['teams']=teams
        for i in range(len(teams)):
            self.context['teams'][i].initializeField(i)

    def runBattle(self):
        queue=BattleQueue()
        self.context['turn']=1
        while True:
            # return winning team if that team is only team that remains
            remainingTeams=[i for i in range(len(self.context['teams'])) if not self.context['teams'][i].isWhiteOut()]
            if len(remainingTeams)==1:
                return remainingTeams[0]
            
            # if no active pokemon, send out new pokemon
            for team in self.context['teams']:
                team.populateEmptySlots()

            for team in self.context['teams']:
                team.printActivePokemon()

            # choose moves                                 TODO: allow for other options like run, bag, etc
            for team in self.context['teams']:
                actions=team.selectActions(self.context)
                for action in actions:
                    queue.push(action)
                
            # enact moves by speed of pokemon              TODO: change to max heap to handle multi-battles
            queue.executeTurn(self.context)
            self.context['turn']+=1