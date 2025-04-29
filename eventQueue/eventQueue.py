from globals import *
from heapq import heappush, heappop
from collections import defaultdict
from eventQueue.eventAction import EventAction

class EventQueue:
    """Handles event actions put into the queue and executes them in a specific order.

    This class holds all the event actions to be done in Battle. It can execute these actions in order
    based on the lowest EventAction. AKA compares in this order: Turn, Priority

    Attributes:
        eventsDict (dict): Dictionary that holds all event actions scheduled by trigger
    """
    def __init__(self):
        self.eventsDict=defaultdict(list)

    def schedule(self, battleContext, event, trigger):
        """Schedule event to be triggered in the future
        
        Arguments:
            event (Event): Event to be triggered in the future
            turn (int): Turn to trigger event on
            trigger (Trigger): Which trigger to trigger event on
        """
        heappush(self.eventsDict[trigger], EventAction(event=event, turn=battleContext.turn, priority=event.priority))

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
            e.execute(battleContext=battleContext, eventContext=eventContext, trigger=trigger)
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