from entities.trainer import *
from globals import *
from gui import *
from tabulate import tabulate
from battle.battleAction import BattleLocation
class Team:
    """Represents team in a battle.

    Attributes:
        trainers (list): List of trainers on team
        teamName (str): Name of team
        teamIdx (int): Index of team in battle context
        fieldSize (int): Number of slots on battlefield this team has
        slots (list): List of BattleLocations

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
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
            self.slots.append(BattleLocation(teamIdx, i))

    def bindRelationships(self):
        """Stores the team in each trainer and each trainer in each pokemon, binding the relationships between them."""
        for trainer in self.trainers:
            trainer.bindRelationships(self)

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
        validTrainers=[trainer for trainer in self._getAliveTrainers() if len(trainer.getBenchedPokemon())>0]
        trainerNames=[DropdownItem(trainer.name, i) for i, trainer in enumerate(validTrainers)]

        if len(validTrainers)==1:
            return validTrainers[0]
        if len(validTrainers)==0:
            return None

        showDropdown(self.battleContext, team=self.teamIdx, text='Select a trainer:', values=trainerNames)
        v=waitForSubmit(self.battleContext, self.teamIdx)
        hideDropdown(self.battleContext, team=self.teamIdx)

        return validTrainers[v[f'team{self.teamIdx+1}DDChoice'].id]
    
    def populateEmptySlots(self):
        """Populates all slots without pokemon in them."""
        self.battleContext.currentTeam=self.teamIdx
        for i, slot in enumerate(self.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                trainer=self.selectTrainer()
                if trainer is None:
                    slot.clear()
                    self.battleContext.window[f'team{self.teamIdx+1}:{i}PokemonName'].update(value=f'Name: {'N/A'}')
                    self.battleContext.window[f'team{self.teamIdx+1}:{i}HP'].update(value=f'HP: {'N/A'}')
                    refreshWindow(self.battleContext)
                    continue
                pokemon=trainer.selectPokemon()
                slot.swapPokemon(trainer, pokemon)

                self.battleContext.window[f'team{self.teamIdx+1}:{i}PokemonName'].update(value=f'Name: {pokemon.name}')
                self.battleContext.window[f'team{self.teamIdx+1}:{i}HP'].update(value=f'HP: {pokemon.stats.currentHP}')
                refreshWindow(self.battleContext)

    def selectActions(self):
        """Selects actions for each slot."""
        actions=[]
        self.battleContext.currentTeam=self.teamIdx
        for slot in self.slots:
            if slot.pokemon is None:
                continue
            actions.append(slot.selectAction())
        return actions
    
    # Enforces that battleContext is set before used
    @property
    def battleContext(self):
        if not hasattr(self, '_battleContext') or self._battleContext is None:
            raise AttributeError(f'{self.__class__.__name__} is missing battleContext.')
        return self._battleContext
    
    @battleContext.setter
    def battleContext(self, val):
        self._battleContext=val

    def setBattleContext(self, battleContext):
        """Sets battle context"""
        self.battleContext=battleContext
        for trainer in self.trainers:
            trainer.setBattleContext(battleContext)