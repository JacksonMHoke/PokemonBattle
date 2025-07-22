from battle.battleAction import *
from globals import *
from heapq import heappush, heappop

class BattleQueue:
    """Handles actions put into the queue and executes them in a specific order.

    This class holds all the actions to be done in Battle. It can execute these actions in order
    based on the lowest BattleAction. AKA compares in this order: Turn, Priority, Speed

    Attributes:
        pq (list): Priority queue that holds all actions

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
    """
    def __init__(self):
        self.pq=[]

    def push(self, action):
        """Pushes action onto queue"""
        heappush(self.pq, action)

    def executeAction(self):
        """Executes next BattleAction"""
        action=self.pq[0]
        heappop(self.pq)
        action.execute(self.battleContext)

    def executeTurn(self):
        """Executes all actions in the current turn"""
        if len(self.pq)==0:
            return
        
        currentTurn=self.battleContext.turn
        while len(self.pq)>0 and self.pq[0].turn==currentTurn:
            self.executeAction()

        self.battleContext.eventSystem.trigger(eventContext=None, trigger=Trigger.END_TURN)
        self.battleContext.eventSystem.trigger(eventContext=None, trigger=Trigger.END_TURN_STATUS)

    # Enforces that battleContext is set before used
    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, battleContext):
        """Sets battle context"""
        self._battleContext=battleContext