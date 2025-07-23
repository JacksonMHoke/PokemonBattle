from statuses.status import *
from events.events import *
from utils import *
from stats.statBuff import *
from globals import *

class Paralyzed(Status):
    """
    Paralyzed status. Paralyzed pokemon are slowed and have a chance to have their moves be canceled.
    """
    def __init__(self):
        super().__init__(name=self.__class__.__name__, color='yellow')
        self.paralyzedChance=0.3
        self.speedDebuff=0.5
        self.event=None
        self.debuff=None

    def inflictStatus(self, pokemon, battleContext):
        self.inflictedPokemon=pokemon
        self.event=PreventMoveByChance(preventChance=self.paralyzedChance, target=pokemon)
        battleContext.eventSystem.addPermanentEvent(self.event)

        self.debuff=StatBuff(name='Paralyzed Slow', flat=0, mult=-0.5)
        pokemon.stats.addBuff(self.debuff, 'Spe')

    def cureStatus(self, battleContext):
        battleContext.eventSystem.remove(matchById(self.event))
        self.inflictedPokemon.removeBuffs(matchById(self.debuff))
        self.inflictedPokemon=None
