from globals import *
from heapq import heappush, heappop
from collections import defaultdict

class EventQueue:
    """Handles event actions put into the queue and executes them in a specific order.

    This class holds all the event actions to be done in Battle. It can execute these actions in order
    based on the lowest EventAction. AKA compares in this order: Turn, Priority

    Attributes:
        eventsDict (dict): Dictionary that holds all event actions scheduled by trigger
    """
    def __init__(self):
        self.eventsDict=defaultdict(list)

    def push(self, event, trigger):
        """Push event onto the queue for specific trigger
        
        Arguments:
            event (Event): Event to be triggered in the future
            trigger (Trigger): Which trigger to trigger event on
        """
        print(f'EVENTQUEUE SCHEDULE {event.name}')
        heappush(self.eventsDict[trigger], event)

    def top(self, trigger):
        """Return next event in queue for specified trigger.
        
        Arguments:
            trigger (Trigger): Which trigger to get next event for

        Returns:
            Event
        """
        if len(self.eventsDict[trigger])==0:
            return None
        return self.eventsDict[trigger][0]
    
    def pop(self, trigger):
        """Remove top event in queue for specified trigger
        
        Arguments:
            trigger (Trigger): Which trigger to remove the next event for
        """
        if len(self.eventsDict[trigger]==0):
            print(f'EventQueue: Tried to pop from empty list. Trigger: {trigger.name}')
            return
        heappop(self.eventsDict[trigger])

    def empty(self, trigger):
        """Returns true if there are no events for specified trigger
        
        Arguments:
            trigger (Trigger): Which trigger to check emptiness for

        Returns:
            Bool
        """
        return len(self.eventsDict[trigger])<=0

    def trigger(self, battleContext, eventContext, trigger):
        """Triggers all events scheduled for trigger passed in
        
        Triggers all events scheduled for trigger passed in and fills eventContext with any information
        to be used outside of event trigger.

        Arguments:
            context (Context): Context of the battle
            eventContext (EventContext): Event context
            trigger (Trigger): Trigger to activate events for
        """
        while len(self.eventsDict[trigger])>0 and self.eventsDict[trigger][0].turn==battleContext.turn:
            e=self.eventsDict[trigger][0]
            heappop(self.eventsDict[trigger])
            e.trigger(battleContext=battleContext, eventContext=eventContext, trigger=trigger)
        if battleContext.weather is not None:
            battleContext.weather.trigger(battleContext=battleContext, eventContext=eventContext, trigger=trigger)
        
    
def scheduleAllEvents(battleContext):
    """Schedule all events"""
    for team in battleContext.teams:
        for trainer in team.trainers:
            for pokemon in trainer.party:
                for event in [pokemon.item, pokemon.ability, pokemon.status]:   
                    if event is None:
                        continue
                    if event.name=='Sword':
                        event.schedule(battleContext)
                        continue
                    for trigger in event.triggers:
                        battleContext.eventQueue.schedule(battleContext=battleContext, event=event, trigger=trigger)
    for event in battleContext.events:
        for trigger in event.triggers:
            event.eventQueue.schedule(battleContext=battleContext, event=event, trigger=trigger)
    if battleContext.weather is not None:
        for trigger in battleContext.weather.triggers:
            battleContext.eventQueue.schedule(battleContext=battleContext, event=battleContext.weather, trigger=trigger)

def scheduleEventAllTriggers(battleContext, event):
    for trigger in event.triggers:
        battleContext.eventQueue.schedule(battleContext=battleContext, event=event, trigger=trigger)