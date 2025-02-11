from trainer import *
from globals import *
from tabulate import tabulate
class Team:
    def __init__(self, name, trainers, slots=1):
        self.trainers=trainers
        self.teamName=name
        self.slots=[None]*slots
    
    def isWhiteOut(self):
        return all([trainer.isWhiteOut() for trainer in self.trainers])
    
    def populateEmptySlots(self):
        for slot in self.slots:
            if slot is None:
                trainer=self.selectTrainer()
                slot=trainer.selectPokemon()

    def printActivePokemon(self):
        names=[mon.name if mon is not None else "empty" for mon in self.slots]
        hps=[mon.stats[Stat.HP] if mon is not None else "N/A" for mon in self.slots]
        print(self.teamName)
        print(tabulate([names, hps]))

    def selectActions(self):
        actions=[]
        for trainer in self.trainers:
            actions.extend(trainer.selectMoves())
        return actions
