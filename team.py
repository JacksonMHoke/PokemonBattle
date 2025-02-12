from trainer import *
from globals import *
from tabulate import tabulate
class Team:
    def __init__(self, name, trainers, fieldSize=1):
        self.trainers=trainers
        self.teamName=name
        self.teamIdx=-1
        self.fieldSize=fieldSize
        self.slots=[]

    def initializeField(self, teamIdx):
        self.teamIdx=teamIdx
        for i in range(self.fieldSize):
            self.slots.append(BattleLocation(teamIdx, i, None, None))

    def _getAliveTrainers(self):
        return [trainer for trainer in self.trainers if not trainer.isWhiteOut()]

    def isWhiteOut(self):
        return len(self._getAliveTrainers())==0
    
    def selectTrainer(self):                                        # TODO: ENSURE THERE ARE POKEMON TO CHOOSE FROM IN CHOICES AVAILABLE
        validTrainers=self._getAliveTrainers()
        print('List of possible trainers: ', flush=True)
        for i, trainer in enumerate(validTrainers):
            print('\t', i, trainer.name, flush=True)
        try:
            choice=int(input('Select the trainer you want to choose: '))
        except:
            return self.selectPokemon()
        choice=clamp(choice, 0, len(validTrainers)-1)
        return validTrainers[choice]
    
    def populateEmptySlots(self):
        for i, slot in enumerate(self.slots):
            if slot.pokemon is None:
                trainer=self.selectTrainer()
                pokemon=trainer.selectPokemon()
                slot.swapPokemon(trainer, pokemon)

    def printActivePokemon(self):
        names=[slot.pokemon.name for slot in self.slots if slot.pokemon is not None]
        hps=[slot.pokemon.stats[Stat.HP] for slot in self.slots if slot.pokemon is not None]
        print(self.teamName)
        print(tabulate([names, hps]))
        print('\n', flush=True)

    def selectActions(self, context):
        actions=[]
        for slot in self.slots:
            actions.append(slot.selectAction(context))
        return actions
