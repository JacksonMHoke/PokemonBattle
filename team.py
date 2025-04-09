from trainer import *
from globals import *
from gui import *
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
    
    def selectTrainer(self, context):                                        # TODO: Separate this into generic select trainer and select trainer for benched pokemon
        """Selects trainer that is not whited out.
        
        Returns:
            Trainer: Selected trainer
        """
        validTrainers=[trainer for trainer in self._getAliveTrainers() if len(trainer.getBenchedPokemon())>0]
        trainerNames=[trainer.name for trainer in validTrainers]
        if len(validTrainers)==1:
            return validTrainers[0]
        context.window[f'team{self.teamIdx+1}DDChoice'].update(values=trainerNames)
        context.window[f'team{self.teamIdx+1}DD'].update(visible=True)
        context.window.refresh()
        v=waitForSubmit(context)
        context.window[f'team{self.teamIdx+1}DD'].update(visible=False)
        for name, trainer in zip(trainerNames, validTrainers):
            if name==v[f'team{self.teamIdx+1}DDChoice']:
                return trainer
        raise Exception('No match in trainer dropdown')
    
    def populateEmptySlots(self, context):
        """Populates all slots without pokemon in them."""
        context.currentTeam=self.teamIdx
        for i, slot in enumerate(self.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                trainer=self.selectTrainer(context)
                pokemon=trainer.selectPokemon(context)
                slot.swapPokemon(trainer, pokemon)

                context.window[f'team{self.teamIdx+1}PokemonName'].update(value=f'Name: {pokemon.name}')
                context.window[f'team{self.teamIdx+1}HP'].update(value=f'HP: {pokemon.stats[Stat.HP]}')
                context.window.refresh()

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
        context.currentTeam=self.teamIdx
        for slot in self.slots:
            actions.append(slot.selectAction(context))
        return actions