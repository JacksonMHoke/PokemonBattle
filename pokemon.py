from globals import Stat
from globals import Type
class Pokemon:
    def __init__(self, name, typing, level, stats, moves, ability=None):
        self.name=name
        self.typing=typing
        self.stats=stats
        self.moves=moves
        self.ability=ability
        self.fainted=False
        self.level=level
        self.exp=0
        self.hp=stats[Stat.MHP]
