from trainer import *
from globals import *
from tabulate import tabulate
class Team:
    """Represents team in a battle.

    Attributes:
        trainers (list): List of trainers on team
        teamName (str): Name of team
        teamIdx (int): Index of team in battle context
        fieldSize (int): Number of slots on battlefield this team has
        slots (list): List of BattleLocations

    Note:
        Do not modify teamIdx
    """
    def __init__(self, name, trainers, fieldSize=1):
        self.trainers=trainers
        self.teamName=name
        self.teamIdx=-1
        self.fieldSize=fieldSize
        self.slots=[]

    def initializeField(self, teamIdx):
        """Sets the field for this team.

        Arguements:
            teamIdx (int): Index of team in battle context
        """
        self.teamIdx=teamIdx
        for i in range(self.fieldSize):
            self.slots.append(BattleLocation(teamIdx, i, None, None))

    def _getAliveTrainers(self):
        return [trainer for trainer in self.trainers if not trainer.isWhiteOut()]

    def isWhiteOut(self):
        """Returns if team is whited out."""
        return len(self._getAliveTrainers())==0
    
    def selectTrainer(self):                                        # TODO: Separate this into generic select trainer and select trainer for benched pokemon
        """Selects trainer that is not whited out.
        
        Returns:
            Trainer: Selected trainer
        """
        validTrainers=self._getAliveTrainers()
        print('List of possible trainers: ', flush=True)
        for i, trainer in enumerate(validTrainers):
            if len(trainer.getBenchedPokemon())==0:
                continue
            print('\t', i, trainer.name, flush=True)
        try:
            choice=int(input('Select the trainer you want to choose: '))
        except:
            return self.selectPokemon()
        choice=clamp(choice, 0, len(validTrainers)-1)
        return validTrainers[choice]
    
    def populateEmptySlots(self):
        """Populates all slots without pokemon in them."""
        print('Choose which trainer you would like to select to send a pokemon out: ')
        for i, slot in enumerate(self.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                trainer=self.selectTrainer()
                pokemon=trainer.selectPokemon()
                slot.swapPokemon(trainer, pokemon)

    def printActivePokemon(self):
        """Prints all active pokemon."""
        names=[slot.pokemon.name for slot in self.slots if slot.pokemon is not None]
        hps=[slot.pokemon.stats[Stat.HP] for slot in self.slots if slot.pokemon is not None]
        print(self.teamName)
        print(tabulate([names, hps]))
        print('\n', flush=True)

    def selectActions(self, context):
        """Selects actions for each slot.
        
        Arguments:
            context (Context): Battle context
        """
        actions=[]
        for slot in self.slots:
            actions.append(slot.selectAction(context))
        return actions
