from pokemon import Pokemon
class Trainer:
    def __init__(self, name, party, bag):
        self.name=name
        self.party=party
        self.bag=bag
        self.activePokemon=[]

    def selectAction(self, i): # TODO ADD TARGET SELECTION HERE AS WELL BY FINDING POSITION OF POKEMON AND THROWING THAT INTO MOVE'S SELECT FUNCTION
        print(f'{self.name} is picking a move for {self.activePokemo[i].name}', flush=True)
        try:
            validMoves=self.activePokemon[i].moves
            print('List of moves:', len(validMoves), flush=True)
            for i, move in enumerate(validMoves):
                print('\t', i+1, move.name, flush=True)
            choice=int(input('Select the move by number: '))
        except:
            return self.selectAction()
        selectedMove=validMoves[min(max(0, choice-1), len(validMoves)-1)]
        print(f'{selectedMove.name} was selected.', flush=True)
        return selectedMove
    
    def selectActions(self):
        actions=[]
        for i in range(len(self.activePokemon)):
            actions.append(self.selectAction(i))
        return actions

    
    def _getAlivePokemon(self):
        return [mon for mon in self.party if not mon.fainted]
    
    def selectPokemon(self):
        try:
            validPokemon=self._getAlivePokemon()
            print('List of possible pokemon: ', flush=True)
            for i, mon in enumerate(validPokemon):
                print('\t', i+1, mon.name, flush=True)
            choice=int(input('Select the pokemon you want to send out by number: '))
        except:
            return self.selectPokemon()
        self.activePokemon.append(validPokemon[min(max(0, choice-1), len(validPokemon)-1)])
        return self.activePokemon[-1]
    
    def updateActivePokemon(self):
        for mon in self.activePokemon:
            if mon.fainted:
                self.activePokemon=None

    def isWhiteOut(self):
        return len([mon for mon in self.party if not mon.fainted])==0