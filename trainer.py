from pokemon import Pokemon
class Trainer:
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
        self.activePokemon=None
        self.alivePokemon=len(self.pokemon)

    def selectMove(self):
        assert self.activePokemon is not None
        try:
            validMoves=self.alivePokemon.moves
            print('List of moves:')
            for i, move in enumerate(validMoves):
                print('\t', i+1, move.name)
            choice=int(input('Select the move by number: '))
        except:
            return self.selectMove()
        return validMoves[min(max(0, choice), len(validMoves))]
    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if not mon.fainted]
    
    def selectPokemon(self):
        assert self.alivePokemon>0
        try:
            validPokemon=self._getAlivePokemon()
            print('List of possible pokemon: ')
            for i, mon in enumerate(validPokemon):
                print('\t', i+1, mon.name)
            choice=int(input('Select the pokemon you want to send out by number: '))
        except:
            return self.selectPokemon()
        return validPokemon[min(max(0, choice-1), len(validPokemon)-1)]