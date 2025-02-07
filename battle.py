from trainer import *
from pokemon import *
from moves import *
from random import random

class Battle:
    def __init__(self, trainer1, trainer2):
        self.trainer1=trainer1
        self.trainer2=trainer2
        self.context={}
        self.context['trainer1']=trainer1
        self.context['trainer2']=trainer2

    def _trainer1GoesFirst(self):
        t1Speed=self.trainer1.activePokemon.speed
        t2Speed=self.trainer2.activePokemon.speed
        if t1Speed>t2Speed:
            return True
        if t2Speed>t1Speed:
            return False
        return random()>0.5

    def run_battle(self):
        while True:
            # check if battle should continue
            if self.trainer1.alivePokemon==0:
                return False
            if self.trainer2.alivePokemon==0:
                return True
            
            # if no active pokemon, send out new pokemon
            if self.trainer1.activePokemon is None:
                self.trainer1.selectPokemon()
            if self.trainer2.activePokemon is None:
                self.trainer2.selectPokemon()

            # choose moves                                 TODO: allow for other options like run, bag, etc
            t1Move=self.trainer1.selectMove()
            t2Move=self.trainer2.selectMove()

            # enact moves by speed of pokemon              TODO: change to max heap to handle multi-battles
            if self._trainer1GoesFirst():
                t1Move.enact(self.context, 1)
                if self.trainer2.activePokemon is not None:
                    t2Move.enact(self.context, 2)
            else:
                t2Move.enact(self.context, 2)
                if self.trainer1.activePokemon is not None:
                    t1Move.enact(self.context, 1)