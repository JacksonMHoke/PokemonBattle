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

    def runBattle(self):
        queue=BattleQueue()
        while True:
            # return winning team if that team is only team that remains
            remainingTeams=[i for i in range(len(self.context['teams'])) if self.context['teams'][i].teamWhiteOut(i)]
            if len(remainingTeams)==1:
                return remainingTeams[0]
            
            # if no active pokemon, send out new pokemon
            for team in self.context['teams']:
                team.populateEmptySlots()

            for team in self.context['teams']:
                team.printActivePokemon()

            # choose moves                                 TODO: allow for other options like run, bag, etc
            for team in self.context['teams']:
                actionRequests=team.selectAction()
                for actionRequest in actionRequests:
                    queue.push(actionRequest)
                
            # enact moves by speed of pokemon              TODO: change to max heap to handle multi-battles
            queue.processTurn()