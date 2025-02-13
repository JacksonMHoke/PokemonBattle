from battleaction import *
from heapq import heappush, heappop
class BattleQueue:
    """Handles actions put into the queue and executes them in a specific order.

    This class holds all the actions to be done in Battle. It can execute these actions in order
    based on the lowest BattleAction. AKA compares in this order: Turn, Priority, Speed

    Attributes:
        N/A
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

    def executeTickEvents(self, context):
        """Processes all end of turn tick events such as burn, leech seed, etc."""
        pass

    def executeTurn(self, context):
        """Executes all actions in the current turn"""
        if len(self.pq)==0:
            return
        
        currentTurn=self.pq[0].turn
        while len(self.pq)>0 and self.pq[0].turn==currentTurn:
            self.executeAction(context)

        self.executeTickEvents(context)
        # TODO: Make this function compatible with tick events like leech seed
            # could create an interface class that requires a tick() function to be defined
            # could keep a list of these tick classes in a context dictionary so that we can check if an effect is active