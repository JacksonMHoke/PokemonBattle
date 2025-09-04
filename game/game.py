from battle.battle import Battle

class Game:
    """
    Class for the main gameplay loop of the game.
    """
    def __init__(self):
        self.scaling=1
        self.battles=1
        self.battlesBeforeBoss=5
        self.enemyTeam=None
        self.team=None

    def setupTeam(self):
        pass

    def generateEnemyTeam(self):
        pass

    def generateBossTeam(self):
        pass

    def battle(self):
        """Run battle between enemy team and player team"""
        b=Battle([self.team, self.enemyTeam])
        return b.runBattle()

    def chooseReward(self):
        pass

    def run(self):
       """Run game"""
       self.setupTeam()
       while True:
            self.enemyTeam=self.generateEnemyTeam() if self.battles%self.battlesBeforeBoss else self.generateBossTeam()
            if not self.battle():
               print('Game Over!')
               return 0
            self.chooseReward()
            self.scaling+=0.1
            self.battles+=1