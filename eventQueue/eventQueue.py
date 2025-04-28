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
        self.eventsDict=defaultdict([])

    def schedule(self, context, event, trigger):
        """Schedule event to be triggered in the future
        
        Arguments:
            event (Event): Event to be triggered in the future
            turn (int): Turn to trigger event on
            trigger (Trigger): Which trigger to trigger event on
        """
        heappush(self.eventsDict[trigger], EventAction(event=event, turn=context.turn, priority=event.priority))

    def trigger(self, context, eventContext, trigger):
        """Triggers all events scheduled for trigger passed in
        
        Triggers all events scheduled for trigger passed in and fills eventContext with any information
        to be used outside of event trigger.

        Arguments:
            context (Context): Context of the battle
            eventContext (EventContext): Event context
            trigger (Trigger): Trigger to activate events for
        """
        while len(self.eventsDict[trigger])>0 and self.eventsDict[trigger][0].turn==context.turn:
            e=self.eventsDict[trigger][0]
            heappop(self.eventsDict[trigger])
            e.trigger(context=context, eventContext=eventContext, trigger=trigger)
    
def scheduleAllEvents(context):
    """Schedule all events"""
    for team in context.teams:
        for trainer in team.trainers:
            for pokemon in trainer.party:
                for event in [pokemon.item, pokemon.ability, pokemon.status]:   
                    if event is None:
                        continue
                    for trigger in event.triggers:
                        context.eventQueue.schedule(context=context, event=event, trigger=trigger)
    for event in context.events:
        for trigger in event.triggers:
            event.eventQueue.schedule(context=context, event=event, trigger=trigger)
    if context.weather is not None:
        for trigger in context.weather.triggers:
            context.eventQueue.schedule(context=context, event=context.weather, trigger=trigger)

def scheduleForAllTriggers(context, event):
    for trigger in event.triggers:
        context.eventQueue.schedule(context=context, event=event, trigger=trigger)