from abc import ABC, abstractmethod

class Effect(ABC):
    def __init__(self, triggers):
        self.triggers=triggers

    def trigger(self):
        pass

class Item(ABC, Effect):
    def __init__(self, name, triggers):
        super.__init__(triggers)
        self.name=name

class Ability(ABC, Effect):
    def __init__(self, name, triggers):
        super.__init__(triggers)
        self.name=name
