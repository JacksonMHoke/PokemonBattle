from globals import *

class Item:
    """
    Item that triggers in battle

    Attributes:
        name (str): Name of item
        owner (Pokemon): Owner of item
        id (int): Unique Id
    """
    def __init__(self, name, owner=None):
        self.name=name
        self.owner=owner
        self.id=getUniqueID()

    def attach(self, newOwner, **kwargs):
        """Attach item to pokemon"""

    def detach(self, **kwargs):
        """Detach from current owner"""
        pass

    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, battleContext):
        """Sets battle context"""
        self._battleContext=battleContext