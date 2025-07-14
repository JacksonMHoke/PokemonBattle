from events.eventQueue import *
from events.eventUtils import *
from collections import defaultdict
from collections.abc import Iterable

class EventSystem:
    """Event System that handles the scheduling and triggering of events. Allows
    for adding of permanent and temporary events with duration and proc lifetimes.
    Duration, start turns, and proc lifetimes are handled inside the Event class.

    Attributes:
        scheduledEvents (dict [Trigger: list[Event]]): Dictionary that keeps track of which temporary events are mapped to which trigger.
        permanentEvents (dict [Trigger: list[Event]]): Dictionary that keeps track of which permanent events are mapped to which trigger.

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
    """
    def __init__(self):
        self.scheduledEvents=defaultdict(list)
        self.permanentEvents=defaultdict(list)
        
    def addPermanentEvent(self, event, triggers=None):
        """Adds a permanent event to the EventSystem that will be fired when the triggers are activated.
        If no triggers are passed in, the event's default triggers will be used.

        Arguments:
            event (Event): Event to be added as a permanent event
            triggers (list[Trigger] or Trigger): Trigger/s to add event to
        """
        if triggers is None:
            triggers=event.triggers
        if not isinstance(triggers, Iterable):
            triggers=[triggers]

        for trigger in triggers:
            self.permanentEvents[trigger].append(event)

    def removePermanentEvent(self, shouldRemoveFn, triggers=None):
        """Removes all permanent events from the specified triggers that satisfy the removal function.
        If no triggers are passed in, it will remove from all triggers.

        Arguments:
            shouldRemoveFn (Callable[[Event], bool]): Function used to determine whether to remove event or not
            triggers (list[Trigger] or Trigger): Trigger/s to remove events from
        """
        if triggers is None:
            triggers=self.scheduledEvents.keys()
        if not isinstance(triggers, Iterable):
            triggers=[triggers]

        for trigger in triggers:
            self.permanentEvents[trigger]=[e for e in self.permanentEvents[trigger] if shouldRemoveFn(e)]

    def schedule(self, event, triggers=None):
        """Schedules a temporary event to the EventSystem that will be fired when the triggers are activated.
        If no triggers are passed in, the event's default triggers will be used. Events will only be triggered
        when the turn is in the range [startTurn, startTurn+duration) of the event.

        Arguments:
            event (Event): Event to be added as a temporary event
            triggers (list[Trigger] or Trigger): Trigger/s to add event to
        """
        if triggers is None:
            triggers=event.triggers
        if not isinstance(triggers, Iterable):
            triggers=[triggers]

        if event.startTurn+event.duration-1<self.battleContext.turn:
            return
        
        for trigger in triggers:
            self.scheduledEvents[trigger].append(event)

    def unschedule(self, shouldRemoveFn, triggers=None):
        """Removes all temporary events from the specified triggers that satisfy the removal function.
        If no triggers are passed in, it will remove from all triggers

        Arguments:
            shouldRemoveFn (Callable[[Event], bool]): Function used to determine whether to remove event or not
            triggers (list[Trigger] or Trigger): Trigger/s to remove events from
        """
        if triggers is None:
            triggers=self.scheduledEvents.keys()
        if not isinstance(triggers, Iterable):
            triggers=[triggers]
            
        for trigger in triggers:
            self.scheduledEvents[trigger]=[e for e in self.scheduledEvents[trigger] if shouldRemoveFn(e)]

    def remove(self, shouldRemoveFn, triggers=None):
        """Removes all temporary and permanent events from the specified triggers that satisfy the removal function.
        If no triggers are passed in, it will remove from all triggers
        
        Arguments:
            shouldRemoveFn (Callable[[Event], bool]): Function used to determine whether to remove event or not
            triggers (list[Trigger] or Trigger): Trigger/s to remove events from
        """
        self.removePermanentEvent(shouldRemoveFn=shouldRemoveFn, triggers=triggers)
        self.unschedule(shouldRemoveFn=shouldRemoveFn, triggers=triggers)

    def _populateQueue(self, eventQueue, trigger):
        """Populates eventQueue with all events that should be added in for the trigger specified.
        
        Arguments:
            eventQueue (EventQueue): EventQueue to populate
            trigger (Trigger): The trigger to populate the queue for
        """
        for event in self.scheduledEvents[trigger]:
            if event.startTurn<=self.battleContext.turn<=event.startTurn+event.duration-1:
                eventQueue.push(event)

        for event in self.permanentEvents[trigger]:
            eventQueue.push(event)

    def trigger(self, eventContext, trigger):
        """Triggers the specified event type, evaluating all active scheduled and permanent events.
        Each event may modify the battle or event context. Events with depleted procs are removed.

        Arguments:
            eventContext (EventContext): Context relating to the events. Events modify this to interact with outside code.
            trigger (Trigger): The trigger to activate
        """
        currTurn=self.battleContext.turn
        eq=EventQueue()
        self._populateQueue(eventQueue=eq, trigger=trigger)

        while not eq.empty():
            event=eq.top()
            eq.pop()
            if event.trigger(battleContext=self.battleContext, eventContext=eventContext, trigger=trigger):
                event.procs-=1
                if event.procs<=0:
                    self.remove(matchById(event), event.triggers)

        if trigger==Trigger.END_TURN:
            for trig, events in self.scheduledEvents.items():
                self.scheduledEvents[trig]=[e for e in events if e.startTurn+e.duration-1>currTurn]

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