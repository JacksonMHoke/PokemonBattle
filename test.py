from battle import *
from trainer import *
from pokemon import *
from moves import *
from globals import *
from team import *
from event import *

moves=[Tackle(), Freeze(), Thunder(), Burn(), Earthquake(), ThunderWave(), Rest()]
pikachuStats={
    Stat.HP : 200,
    Stat.ATT : 100,
    Stat.DEF : 100,
    Stat.SPA : 100,
    Stat.SPD : 100,
    Stat.SPE : 100
}
pikachus=[Pikachu('pika1', 15, pikachuStats, moves)]#, Pikachu('pika2', 15, pikachuStats, moves), Pikachu('pika3', 15, pikachuStats, moves), Pikachu('pika4', 15, pikachuStats, moves)]

ratStats={
    Stat.HP : 200,
    Stat.ATT : 100,
    Stat.DEF : 100,
    Stat.SPA : 100,
    Stat.SPD : 100,
    Stat.SPE : 101
}
rats=[Rattata('rat1', 20, ratStats, moves, Sword())]#, Rattata('rat2', 20, ratStats, moves), Rattata('rat3', 20, ratStats, moves), Rattata('rat4', 20, ratStats, moves)]
t1=Trainer('Trainer 1', pikachus, None)
t2=Trainer('Trainer 2', rats, None)
# t3=Trainer('Trainer 3', deepcopy(rats[:1]), None)
teams=[Team('Team Pikachu', [t1], 1), Team('Team Rattata', [t2], 1)]#, Team('Team Rats 2.0', [t3], 2)]
testBattle=Battle(teams)

testBattle.runBattle()