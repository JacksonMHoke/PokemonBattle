from globals import *

class Item:
    """
    Item that triggers in battle

    Attributes:
        name (str): name of item
        owner (Pokemon): Owner of item
        timesUsed (int): number of times item has been triggered
    """
    self, triggers, priority=EventPrio.DEFAULT, startTurn=0, duration=1, procs=float('inf')
    def __init__(self, name, triggers, priority=EventPrio.ITEM, startTurn=0, duration=1, procs=float('inf'), owner=None):
        super().__init__(triggers=triggers, priority=priority, startTurn=startTurn, duration=duration, procs=procs)
        self.name=name
        self.owner=owner
        self.timesUsed=0
        self.events=[]

    def attach(self, battleContext, eventContext, pokemon):
        """Attach item to pokemon"""
        pass

    def detach(self, battleContext, eventContext):
        """Detach from current owner"""
        pass