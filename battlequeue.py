from battleaction import *
from event import *
from heapq import heappush, heappop

class BattleQueue:
    """Handles actions put into the queue and executes them in a specific order.

    This class holds all the actions to be done in Battle. It can execute these actions in order
    based on the lowest BattleAction. AKA compares in this order: Turn, Priority, Speed

    Attributes:
        pq (list): Priority queue that holds all actions
    """
    def __init__(self):
        self.pq=[]

    def push(self, action):
        """Pushes action onto queue"""
        heappush(self.pq, action)

    def executeAction(self, context):
        """Executes next BattleAction"""
        action=self.pq[0]
        heappop(self.pq)
        action.execute(context)

    def executeTurn(self, context):
        """Executes all actions in the current turn"""
        if len(self.pq)==0:
            return
        
        currentTurn=self.pq[0].turn
        while len(self.pq)>0 and self.pq[0].turn==currentTurn:
            self.executeAction(context)

        triggerAllEvents(context, Trigger.END_TURN_STATUS)