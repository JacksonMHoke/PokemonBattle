from pokemon import Pokemon
class Trainer:
    def __init__(self, name, pokemon, bag):
        self.name=name
        self.pokemon=pokemon
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