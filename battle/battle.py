from entities.trainer import *
from entities.pokemon import *
from moves.move import *
from battle.battleQueue import *
from contexts.battleContext import *
from contexts.eventContext import *
from gui import *
import FreeSimpleGUI as sg
from tabulate import tabulate
from random import random

class Battle:
    """Represents a battle scenario between teams.

    This class manages the setup and simulation of a battle between separate teams.

    Attributes:
        teams (list): A list of teams to be in battle
        battleContext (battleContext): Battle battleContext
    """
    def __init__(self, teams):
        self.battleContext=BattleContext(teams=teams)
        for i in range(len(teams)):
            self.battleContext.teams[i].bindRelationships()
            self.battleContext.teams[i].initializeField(i)
            self.battleContext.teams[i].setBattleContext(self.battleContext)

    def runBattle(self):
        """Runs the battle."""
        queue=BattleQueue()
        queue.setBattleContext(self.battleContext)
        self.battleContext.attachItems()
        self.battleContext.attachAbilities()
        self.battleContext.turn=1
        
        self.battleContext.window = sg.Window('Battle Window', getLayout(self.battleContext), size=(800, 1080), resizable=True, finalize=True, return_keyboard_events=True, element_justification='center')

        while True:
            # return winning team if that team is only team that remains
            remainingTeams=[team for team in self.battleContext.teams if not team.isWhiteOut()]
            if len(remainingTeams)==1:
                self.battleContext.window['combatLog'].update(f'{remainingTeams[0].teamName} wins!\n', append=True)
                while True:
                    e, v = self.battleContext.window.read(timeout=50)
                    if e == sg.WINDOW_CLOSED or e == "Exit":
                        break
                return remainingTeams[0]
            
            if self.battleContext.turn==0:
                self.battleContext.eventSystem.trigger(eventContext=EventContext(), trigger=Trigger.START)
            
            e, v = self.battleContext.window.read(timeout=50)
            if e == sg.WINDOW_CLOSED or e == "Exit":
                break
            
            # if no active pokemon, send out new pokemon
            for team in self.battleContext.teams:
                team.populateEmptySlots()

            self.battleContext.window['combatLog'].update(f'-------------Turn {self.battleContext.turn}-------------\n', append=True)
            refreshWindow(self.battleContext)

            # choose moves                                 TODO: allow for other options like run, bag, etc
            for team in self.battleContext.teams:
                actions=team.selectActions()
                for action in actions:
                    queue.push(action)
                
            # enact moves in correct order
            queue.executeTurn()

            refreshWindow(self.battleContext)

            self.battleContext.turn+=1