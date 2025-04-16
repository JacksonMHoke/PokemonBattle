from pokemon import *
from battleaction import *
from gui import *
class Trainer:
    """Represents a pokemon trainer

    Attributes:
        name (str): Name of trainer.
        party (list): List of pokemon in party
        bag (Bag): Trainer's bag(TODO: implement bag class)
    """
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if mon.state!=State.FAINTED]

    def getBenchedPokemon(self):
        return [mon for mon in self.party if mon.state==State.BENCHED]
    
    def selectPokemon(self, context): # TODO: create general select function vs select benched pokemon
        """Selects a pokemon from the list of benched pokemon in party."""
        validPokemon=self.getBenchedPokemon()
        pokemonNames=[DropdownItem(pokemon.name, i) for i, pokemon in enumerate(validPokemon)]

        if len(validPokemon)==0:
            return None

        showDropdown(context=context, team=context.currentTeam, text='Select a pokemon to send out:', values=pokemonNames)
        v=waitForSubmit(context, context.currentTeam)
        hideDropdown(context=context, team=context.currentTeam)

        return validPokemon[v[f'team{context.currentTeam+1}DDChoice'].id]

    def isWhiteOut(self):
        """Returns if trainer is whited out."""
        return len(self._getAlivePokemon())==0