from pokemon import *
from battleaction import *
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
    
    def selectPokemon(self):
        """Selects a pokemon from the list of non-fainted pokemon in party."""
        validPokemon=self._getAlivePokemon()
        print('List of possible pokemon: ', flush=True)
        for i, mon in enumerate(validPokemon):
            print('\t', i, mon.name, flush=True)
        try:
            choice=int(input('Select the pokemon you want to send out by number: '))
        except:
            return self.selectPokemon()
        choice=clamp(choice, 0, len(validPokemon)-1)
        print(f'{validPokemon[choice].name} was selected!\n\n', flush=True)
        return validPokemon[choice]

    def isWhiteOut(self):
        """Returns if trainer is whited out."""
        return len(self._getAlivePokemon())==0