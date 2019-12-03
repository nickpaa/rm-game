from pandas import DataFrame
from scipy.stats import gamma, binom
from random import choices


class Game():

    def __init__(self, scenario):

        self.ndfd = scenario.ndfd
        self.fc = scenario.fc
        self.ac = scenario.ac
        self.au = scenario.ac  # start by initializing AU to AC

        self.au = scenario.ac
        self.sa = self.au
        self.total_lb = 0
        self.total_rev = 0
        self.curr_dfd = int(scenario.ndfd)
        self.curr_dow_long = self.fc.loc[self.curr_dfd, 'dow_long']
        self.curr_dow_short = self.fc.loc[self.curr_dfd, 'dow_short']


    def set_player_info(self, player=None, location=None):
        self.player = player
        self.location = location


class EasyGame(Game):

    def __init__(self, scenario):
        Game.__init__(self, scenario)
        self.game_type = 'Easy mode'
        self.easy_mode = True
        self.fc['stdev'] = 0


class RealGame(Game):

    def __init__(self, scenario):
        Game.__init__(self, scenario)
        self.game_type = 'Real life mode'
        self.easy_mode = False
        self.ns_rate = scenario.ns_rate
        self.db_costs = scenario.db_costs

    def simulate_noshows(self):
        return binom.rvs(n=self.total_lb, p=self.ns_rate)

    def compensate_dbs(self):
        return choices(self.db_costs['costs'], weights=self.db_costs['weights'])[0]


class DFDSimulation():

    def __init__(self, game, dfd):
        self.game = game
        self.dfd = dfd
        self.fare = game.fc.loc[dfd, 'fare']
        self.demand = game.fc.loc[dfd, 'demand']
        self.stdev = game.fc.loc[dfd, 'stdev']

    def observe_bookings(self, rsv):
        self.rsv = rsv

        if self.game.easy_mode:
            self.arr = self.demand
        else:
            a = (self.demand ** 2) / (self.stdev ** 2)
            scale = (self.stdev ** 2) / self.demand
            self.arr = int(gamma.rvs(a=a, scale=scale))
        
        self.lb = min(self.arr, self.rsv)
        self.rev = self.lb * self.fare

        self.game.total_rev += self.rev
        self.game.total_lb += self.lb
        self.game.sa -= self.lb

    def dfd_cleanup(self):
        self.game.fc.drop(self.dfd, axis=0, inplace=True)
        self.game.curr_dfd -= 1
        if self.game.curr_dfd >= 0:
            self.game.curr_dow_long = self.game.fc.loc[self.game.curr_dfd, 'dow_long']
            self.game.curr_dow_short = self.game.fc.loc[self.game.curr_dfd, 'dow_short']

