from battleaction import *
from heapq import heappush, heappop
class BattleQueue:
    def __init__(self):
        self.pq=[]

    def push(self, action):
        heappush(self.pq, action)

    def executeAction(self, context):
        action=self.pq[0]
        heappop(self.pq)
        action.execute(context)

    def executeTickEvents(self, context):
        pass

    def executeTurn(self, context):
        if len(self.pq)==0:
            return
        
        currentTurn=self.pq[0].turn
        while len(self.pq)>0 and self.pq[0].turn==currentTurn:
            self.executeAction(context)

        self.executeTickEvents(context)
        # TODO: Make this function compatible with tick events like leech seed
            # could create an interface class that requires a tick() function to be defined
            # could keep a list of these tick classes in a context dictionary so that we can check if an effect is active