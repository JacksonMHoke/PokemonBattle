from pokemon import *
from battleaction import *
class Trainer:
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
        self.activePokemon=[]
    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if not mon.fainted]
    
    def selectPokemon(self):
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
    
    def updateActivePokemon(self):
        for i, mon in enumerate(self.activePokemon):
            if mon.fainted:
                self.activePokemon[i]=None

    def isWhiteOut(self):
        return len(self._getAlivePokemon())==0