from trainer import *
from pokemon import *
from moves import *
from battlequeue import *
from context import *
from event import *
from gui import *
import FreeSimpleGUI as sg
from tabulate import tabulate
from random import random

class Battle:
    """Represents a battle scenario between teams.

    This class manages the setup and simulation of a battle between separate teams.

    Attributes:
        teams (list): A list of teams to be in battle
        context (Context): Battle context
    """
    def __init__(self, teams):
        self.context=Context(teams=teams)
        for i in range(len(teams)):
            self.context.teams[i].initializeField(i)

    def runBattle(self):
        """Runs the battle."""
        queue=BattleQueue()
        self.context.turn=1
        
        self.context.window = sg.Window('Battle Window', getLayout(self.context), size=(800, 600), resizable=True, finalize=True, return_keyboard_events=True, element_justification='center')

        triggerAllEvents(self.context, Trigger.START)   # Triggers all events that are conditional on battle start

        while True:
            # return winning team if that team is only team that remains
            remainingTeams=[team for team in self.context.teams if not team.isWhiteOut()]
            if len(remainingTeams)==1:
                self.context.window['combatLog'].update(f'{remainingTeams[0].teamName} wins!\n', append=True)
                while True:
                    e, v = self.context.window.read(timeout=50)
                    if e == sg.WINDOW_CLOSED or e == "Exit":
                        break
                return remainingTeams[0]
            
            e, v = self.context.window.read(timeout=50)
            if e == sg.WINDOW_CLOSED or e == "Exit":
                break
            
            # if no active pokemon, send out new pokemon
            for team in self.context.teams:
                team.populateEmptySlots(self.context)

            self.context.window['combatLog'].update(f'-------------Turn {self.context.turn}-------------\n', append=True)
            refreshWindow(self.context)

            # choose moves                                 TODO: allow for other options like run, bag, etc
            for team in self.context.teams:
                actions=team.selectActions(self.context)
                for action in actions:
                    queue.push(action)
                
            # enact moves in correct order
            queue.executeTurn(self.context)

            refreshWindow(self.context)

            self.context.turn+=1