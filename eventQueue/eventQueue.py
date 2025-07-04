from globals import *
from heapq import heappush, heappop

class EventQueue:
    """Handles event actions put into the queue and executes them in a specific order.

    This class holds all the event actions to be done in Battle. It can execute these actions in order
    based on the lowest EventAction. AKA compares in this order: Turn, Priority

    Attributes:
        eventsDict (dict): Dictionary that holds all event actions scheduled by trigger
    """
    def __init__(self):
        self.events=list

    def push(self, event):
        """Push event onto the queue
        
        Arguments:
            event (Event): Event to be triggered in the future
        """
        print(f'EVENTQUEUE PUSH {event.name}')
        heappush(self.events, event)

    def top(self):
        """Return next event in queue

        Returns:
            Event
        """
        if self.empty():
            return None
        return self.events[0]
    
    def pop(self):
        """Remove top event in queue"""
        if self.empty():
            print(f'EventQueue: Tried to pop from empty list.')
            return
        heappop(self.events)

    def empty(self, trigger):
        """Returns true if there are no events for specified trigger
        
        Arguments:
            trigger (Trigger): Which trigger to check emptiness for

        Returns:
            Bool
        """
        return len(self.events)<=0