from entities.pokemon import *
from battle.battleAction import *
from gui import *
class Trainer:
    """Represents a pokemon trainer

    Attributes:
        name (str): Name of trainer.
        party (list): List of pokemon in party
        bag (Bag): Trainer's bag(TODO: implement bag class)

        battleContext (BattleContext): Current battle context. Will be set automatically at start of battle
        team (Team): Team. Will be set automatically at start of battle
    """
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if mon.state!=State.FAINTED]

    def getBenchedPokemon(self):
        return [mon for mon in self.party if mon.state==State.BENCHED]
    
    def selectPokemon(self): # TODO: create general select function vs select benched pokemon
        """Selects a pokemon from the list of benched pokemon in party."""
        validPokemon=self.getBenchedPokemon()
        pokemonNames=[DropdownItem(pokemon.name, i) for i, pokemon in enumerate(validPokemon)]

        if len(validPokemon)==0:
            return None

        showDropdown(battleContext=self.battleContext, team=self.battleContext.currentTeam, text='Select a pokemon to send out:', values=pokemonNames)
        v=waitForSubmit(self.battleContext, self.battleContext.currentTeam)
        hideDropdown(battleContext=self.battleContext, team=self.battleContext.currentTeam)

        return validPokemon[v[f'team{self.battleContext.currentTeam+1}DDChoice'].id]

    def isWhiteOut(self):
        """Returns if trainer is whited out."""
        return len(self._getAlivePokemon())==0
    
    def bindRelationships(self, team):
        self.team=team
        for mon in self.party:
            mon.bindRelationships(self)
    
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
        for mon in self.party:
            mon.setBattleContext(battleContext)

    @property
    def team(self):
        if not hasattr(self, '_team') or self._team is None:
            raise AttributeError(f'{self.__class__.__name__} is missing team.')
        return self._team
        
    @team.setter
    def team(self, val):
        self._team=val