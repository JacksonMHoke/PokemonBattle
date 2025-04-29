from battle import *
from entities.trainer import *
from entities.pokemon import *
from moves.moves import *
from globals import *
from entities.team import *
from events.items import *
from events.statuses import *
from events.weathers import *
from battle.battle import *

moves=[Tackle(), Freeze(), Thunder(), Burn(), Earthquake(), ThunderWave(), Rest(), RainDance(), WaterLance(), SwordsDance(), FireBall(), FireSwipe(), Conflagration()]
pikachuStats=Stats(200,100,100,100,100,100)
pikachus=[Pikachu('pika1', 15, pikachuStats, moves)]#, Pikachu('pika2', 15, pikachuStats, moves), Pikachu('pika3', 15, pikachuStats, moves), Pikachu('pika4', 15, pikachuStats, moves)]

ratStats=Stats(200,100,100,100,100,101)
rats=[Rattata('rat1', 20, ratStats, moves)]#, Rattata('rat2', 20, ratStats, moves), Rattata('rat3', 20, ratStats, moves), Rattata('rat4', 20, ratStats, moves)]
rats[0].item=Sword(rats[0])

bellStats=Stats(200, 75, 100, 150, 150, 30)
bell=Bell('Bong', 15, bellStats, moves, None, None)

shroomHogStats=Stats(150, 100, 75, 150, 150, 75)
shroomHog=Shroomhog('SadHog', 15, shroomHogStats, moves)
shroomHog.item=Sword(shroomHog)
t1=Trainer('Trainer 1', [bell, pikachus[0]], None)
t2=Trainer('Trainer 2', [rats[0], shroomHog], None)
teams=[Team('Team Bell', [t1], 1), Team('Team Shrooms', [t2], 1)]
testBattle=Battle(teams)

testBattle.runBattle()

# event context variables so far
# cancelMove
# item (when equipping/unequipping)
# attackMult