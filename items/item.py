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

    def attach(self, battleContext, eventContext, pokemon):
        """Attach item to pokemon"""
        pass

    def detach(self, battleContext, eventContext):
        """Detach from current owner"""
        pass