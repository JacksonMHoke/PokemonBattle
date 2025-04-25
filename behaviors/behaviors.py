from globals import *
from abc import ABC, abstractmethod

class ExecutionBehavior(ABC):
    """Abstract class for move behavior

    This class is an abstract class that requires a single function, do, that executes the desired
    behavior from the attacker to the targets.

    Note: This class is an abstract class and is not to be instantiated
    """
    @staticmethod
    @abstractmethod
    def do(context):
        pass

'''
Selection Behavior
'''
class SelectionBehavior(ABC):
    """Abstract class for selection behavior.

    This class is an abstract class that requires a single function, `select`, that takes in the attacker location and returns
    a list of target locations that are selected from user input. 

    Note:
        This class is an abstract class and is not to be instantiated
    """
    @staticmethod
    @abstractmethod
    def select(context, attackerLoc):
        pass