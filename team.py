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
        trainerNames=[DropdownItem(trainer.name, i) for i, trainer in enumerate(validTrainers)]

        if len(validTrainers)==1:
            return validTrainers[0]
        if len(validTrainers)==0:
            return None

        showDropdown(context=context, team=self.teamIdx+1, text='Select a trainer:', values=trainerNames)
        v=waitForSubmit(context)
        hideDropdown(context=context, team=self.teamIdx+1)

        return validTrainers[v[f'team{self.teamIdx+1}DDChoice'].id]
    
    def populateEmptySlots(self, context):
        """Populates all slots without pokemon in them."""
        context.currentTeam=self.teamIdx
        for i, slot in enumerate(self.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                trainer=self.selectTrainer(context)
                if trainer is None:
                    slot.clear()
                    context.window[f'team{self.teamIdx+1}:{i}PokemonName'].update(value=f'Name: {'N/A'}')
                    context.window[f'team{self.teamIdx+1}:{i}HP'].update(value=f'HP: {'N/A'}')
                    refreshWindow(context)
                    continue
                pokemon=trainer.selectPokemon(context)
                slot.swapPokemon(trainer, pokemon)

                context.window[f'team{self.teamIdx+1}:{i}PokemonName'].update(value=f'Name: {pokemon.name}')
                context.window[f'team{self.teamIdx+1}:{i}HP'].update(value=f'HP: {pokemon.stats[Stat.HP]}')
                refreshWindow(context)

    def selectActions(self, context):
        """Selects actions for each slot.
        
        Arguments:
            context (Context): Battle context
        """
        actions=[]
        context.currentTeam=self.teamIdx
        for slot in self.slots:
            if slot.pokemon is None:
                continue
            actions.append(slot.selectAction(context))
        return actions