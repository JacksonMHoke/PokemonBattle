from pokemon import Pokemon
class Trainer:
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
        self.activePokemon=None
        self.alivePokemon=len(self.party)

    def selectMove(self):
        print(f'{self.name} is picking a move for {self.activePokemon.name}', flush=True)
        assert self.activePokemon is not None
        try:
            validMoves=self.activePokemon.moves
            print('List of moves:', len(validMoves), flush=True)
            for i, move in enumerate(validMoves):
                print('\t', i+1, move.name, flush=True)
            choice=int(input('Select the move by number: '))
        except:
            return self.selectMove()
        selectedMove=validMoves[min(max(0, choice-1), len(validMoves)-1)]
        print(f'{selectedMove.name} was selected.', flush=True)
        return selectedMove
    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if not mon.fainted]
    
    def selectPokemon(self):
        assert self.alivePokemon>0
        try:
            validPokemon=self._getAlivePokemon()
            print('List of possible pokemon: ', flush=True)
            for i, mon in enumerate(validPokemon):
                print('\t', i+1, mon.name, flush=True)
            choice=int(input('Select the pokemon you want to send out by number: '))
        except:
            self.activePokemon=self.selectPokemon()
            return
        self.activePokemon=validPokemon[min(max(0, choice-1), len(validPokemon)-1)]
    
    def updateActivePokemon(self):
        if self.activePokemon.fainted:
            self.activePokemon=None

    def isWhiteOut(self):
        return len([mon for mon in self.party if not mon.fainted])==0