from pandas import DataFrame
from scipy.stats import gamma, binom
from random import choices, sample
from event import *


class Game():

    def __init__(self, scenario):
        self.game_type = scenario.name
        self.game_image_path = scenario.image_path

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
        self.easy_mode = True


class RealGame(Game):

    def __init__(self, scenario):
        Game.__init__(self, scenario)
        self.easy_mode = False
        self.ns_rate = scenario.ns_rate
        self.db_costs = scenario.db_costs
        self.events = scenario.events

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

    def update_demand(self):
        self.game.fc['a'] = (self.game.fc.loc[:, 'demand'] ** 2) / (self.game.fc.loc[:, 'stdev'] ** 2)
        self.game.fc['scale'] = (self.game.fc.loc[:, 'stdev'] ** 2) / self.game.fc.loc[:, 'demand']
        self.game.fc['demand'] = gamma.rvs(a=self.game.fc.loc[:, 'a'], scale=self.game.fc.loc[:, 'scale']).astype(int)
        self.game.fc['stdev'] = self.game.fc.loc[:, 'demand'] * self.game.fc.loc[:, 'cv']

    def dfd_cleanup(self):
        self.game.fc.drop(self.game.curr_dfd, axis=0, inplace=True)
        self.game.curr_dfd -= 1
        if self.game.curr_dfd >= 0:
            if not self.game.easy_mode:
                self.update_demand()
                self.game.fc.loc[:, 'cv'] -= 0.05
            self.game.curr_dow_long = self.game.fc.loc[self.game.curr_dfd, 'dow_long']
            self.game.curr_dow_short = self.game.fc.loc[self.game.curr_dfd, 'dow_short']

    def select_random_event(self):
        self.random_event = sample(self.game.events, 1)[0]
        self.game.events.remove(self.random_event)
        if self.random_event:
            self.dfd_event = self.random_event(self.game)
            self.dfd_event.apply_event()
        else:
            self.dfd_event = None


if __name__ == '__main__':
    from scenario import *
    g = RealGame(RealScenario(scenario_dict[1]))
    d = DFDSimulation(g, 4)
    print(f'dfd {g.curr_dfd}')
    # print(f'ac: {d.game.ac}')
    d.dfd_cleanup()
    d.select_random_event()
    if d.random_event: 
        print(f'applying event {d.dfd_event.name}')
    else:
        print('no event')
    print(f'dfd {g.curr_dfd}')
    # print(f'ac: {d.game.ac}')
    d.dfd_cleanup()
    d.select_random_event()
    if d.random_event: 
        print(f'applying event {d.dfd_event.name}')
    else:
        print('no event')
    print(f'dfd {g.curr_dfd}')
    # print(f'ac: {d.game.ac}')