import pandas as pd
import random
from scipy.stats import norm


class Game():

    def __init__(self, ndfd, data, ac):

        # easy_mode: bool
        # ndfd: int
        # data: dict
        # ac: int

        self.ndfd = int(ndfd)
        self.fc = self.create_forecast(data)
        self.AC = int(ac)
        self.sa = ac
        self.totalrev = 0
        self.curr_dfd = int(ndfd)

    def create_forecast(self, data):
        df = pd.DataFrame(data).set_index('dfd')
        return df

    # def run_game(self):
    #     print()
    #     print('--- THE PRM GAME ---')
    #     for i in range(self.ndfd, -1, -1):
    #         self.curr_dfd = i
    #         self.sim_dfd(self.curr_dfd)
    #     self.summarize_game()

    # def sim_dfd(self, dfd):
        
    #     d = DFDSimulation(self, dfd)

    #     d.run_dfd()

    #     if dfd > 0:
    #         input(f'Your total revenue so far is ${self.totalrev:,}.')
        
    #     self.fc.drop(dfd, axis=0, inplace=True)

    # def summarize_game(self):
    #     lf = int((1 - self.sa / self.AC) * 100)
    #     print()
    #     print(f'The flight has departed. You earned ${self.totalrev:,} and your load factor was {lf}%.')
    #     print()


class EasyGame(Game):

    def __init__(self, ndfd, data, ac):
        Game.__init__(self, ndfd, data, ac)
        self.easy_mode = True
        self.fc['stdev'] = 0


class RealGame(Game):

    def __init__(self, ndfd, data, ac):
        Game.__init__(self, ndfd, data, ac)
        self.easy_mode = False


class DFDSimulation():

    def __init__(self, game, dfd):
        self.game = game
        self.dfd = dfd
        self.fare = game.fc.loc[dfd, 'fare']
        self.demand = game.fc.loc[dfd, 'demand']
        self.stdev = game.fc.loc[dfd, 'stdev']

    def observe_bookings(self, rsv):
        self.rsv = rsv
        self.arr = int(norm.rvs(self.demand, self.stdev))
        self.lb = min(self.arr, self.rsv)
        self.rev = self.lb * self.fare

        self.game.totalrev += self.rev
        self.game.sa -= self.lb

    def dfd_cleanup(self):
        self.game.fc.drop(self.dfd, axis=0, inplace=True)
        self.game.curr_dfd -= 1


class Disruption():
    def __init__(self, game):
        self.name = None
        self.explanation = None

class FareIncrease(Disruption):
    def __init__(self):
        self.name = 'Fare increase disruption'
        self.explanation = 'Increases all future fares by a random amount'

    def apply(self):
        pass


# if __name__ == '__main__':
#     g = EasyGame(dflt_dfd, dflt_fcdata, dflt_ac)
#     g.run_game()

