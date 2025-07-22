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

    def onBattleStart(self):
        """Called once when the battle begins"""

    def attach(self, newOwner, **kwargs):
        """Attach item to pokemon"""
        assert self.owner is None, f'Trying to attach an item({self.name}) that already has an owner.'
        self.owner=newOwner

    def detach(self, **kwargs):
        """Detach from current owner"""
        assert self.owner is not None, f'Trying to detach an item({self.name}) that has no owner.'
        self.owner.item=None
        self.owner=None

    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, battleContext):
        """Sets battle context"""
        self._battleContext=battleContext