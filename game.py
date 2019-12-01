from pandas import DataFrame
from scipy.stats import norm, binom


class Game():

    def __init__(self, scenario):

        self.ndfd = scenario.ndfd
        self.fc = scenario.fc
        self.ac = scenario.ac
        self.au = scenario.ac  # start by initializing AU to AC

        # self.ndfd = int(ndfd)
        # self.fc = self.create_forecast(data)
        # self.AC = int(ac)        

        self.player = None
        self.location = None

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
        self.nsrate = scenario.nsrate

    def simulate_noshows(self):
        return binom.rvs(n=self.total_lb, p=self.nsrate)


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

        self.game.total_rev += self.rev
        self.game.total_lb += self.lb
        self.game.sa -= self.lb

    def dfd_cleanup(self):
        self.game.fc.drop(self.dfd, axis=0, inplace=True)
        self.game.curr_dfd -= 1
        if self.game.curr_dfd >= 0:
            self.game.curr_dow_long = self.game.fc.loc[self.game.curr_dfd, 'dow_long']
            self.game.curr_dow_short = self.game.fc.loc[self.game.curr_dfd, 'dow_short']

