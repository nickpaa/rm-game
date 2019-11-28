import pandas as pd
import random
from scipy.stats import norm


class Game():

    def __init__(self, ndfd, data, ac):

        # easy_mode: bool
        # ndfd: int
        # data: dict
        # ac: int

        self.player = None
        self.location = None
        self.ndfd = int(ndfd)
        self.fc = self.create_forecast(data)
        self.AC = int(ac)
        self.sa = ac
        self.totalrev = 0
        self.curr_dfd = int(ndfd)
        self.curr_dow_long = self.fc.loc[self.curr_dfd, 'dow_long']
        self.curr_dow_short = self.fc.loc[self.curr_dfd, 'dow_short']

    def create_forecast(self, data):
        df = pd.DataFrame(data).set_index('dfd')
        return df

    def set_player_info(self, player=None, location=None):
        self.player = player
        self.location = location


class EasyGame(Game):

    def __init__(self, ndfd, data, ac):
        Game.__init__(self, ndfd, data, ac)
        self.game_type = 'Easy mode'
        self.easy_mode = True
        self.fc['stdev'] = 0


class RealGame(Game):

    def __init__(self, ndfd, data, ac, flight=None):
        Game.__init__(self, ndfd, data, ac)
        self.game_type = 'Real life mode'
        self.game_flight = flight
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
        if self.game.curr_dfd >= 0:
            self.game.curr_dow_long = self.game.fc.loc[self.game.curr_dfd, 'dow_long']
            self.game.curr_dow_short = self.game.fc.loc[self.game.curr_dfd, 'dow_short']


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
