import pandas as pd
import random
from scipy.stats import norm


class Game():

    def __init__(self, ndfd, data, ac, easy_mode=False):

        # easy_mode: bool
        # ndfd: int
        # data: dict
        # ac: int

        self.easy_mode = easy_mode
        self.ndfd = int(ndfd)
        self.fc = self.create_forecast(data)
        self.AC = int(ac)
        self.sa = ac
        self.totalrev = 0
        self.curr_dfd = int(ndfd)


    def create_forecast(self, data):
        df = pd.DataFrame(data).set_index('dfd')
        if self.easy_mode:
            df['stdev'] = 0
            return df
        else:
            return df


    def run_game(self):
        print()
        print('--- THE PRM GAME ---')
        for i in range(self.ndfd, -1, -1):
            self.curr_dfd = i
            self.sim_dfd(self.curr_dfd)
        self.summarize_game()


    def sim_dfd(self, dfd):
        
        d = DFDSimulation(self, dfd)

        d.run_dfd()

        if dfd > 0:
            input(f'Your total revenue so far is ${self.totalrev:,}.')
        
        self.fc.drop(dfd, axis=0, inplace=True)


    def summarize_game(self):
        lf = int((1 - self.sa / self.AC) * 100)
        print()
        print(f'The flight has departed. You earned ${self.totalrev:,} and your load factor was {lf}%.')
        print()


class DFDSimulation():

    def __init__(self, game, dfd):
        self.game = game
        self.dfd = dfd
        #self.fc = game.fc
        self.fare = game.fc.loc[dfd, 'fare']
        self.demand = game.fc.loc[dfd, 'demand']
        self.stdev = game.fc.loc[dfd, 'stdev']
        #self.sa = game.sa


    def run_dfd(self):
        print()
        print(f'--- DFD {self.dfd} ---')
        print(f'There are {self.game.sa} seats remaining.')
        print()
        print('--- FORECAST ---')
        if self.game.easy_mode:
            print(self.game.fc.loc[:, self.game.fc.columns != 'stdev'])
        else:
            print(self.game.fc)
        print()
        
        self.set_au()
        
        self.observe_bookings()

        self.game.sa -= self.lb
        self.game.totalrev += self.rev


    def set_au(self):
        if self.dfd > 0:
            self.au = int(input(f'How many seats do you want to make available for ${self.fare}? '))
            while (self.au > self.game.sa) or (self.au < 0):
                print(f'You can reserve between 0 and {self.game.sa} seats. Reserved seats must be integer values.')
                self.au = int(input(f'How many seats do you want to make available for ${self.fare}? '))
        else:
            input(f'It\'s the last day, so you\'ll reserve all {self.game.sa} seats.')
            self.au = self.game.sa


    def observe_bookings(self):
        self.arr = int(norm.rvs(self.demand, self.stdev))
        self.lb = min(self.arr, self.au)
        input(f'{self.arr} people showed up to book today, and you reserved {self.au} seats.')
        self.rev = self.lb * self.fare
        input(f'You sold {self.lb} seats for ${self.rev:,} in revenue.')


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


fcdata = {
        'dfd': [4,3,2,1,0], 
        'fare':[100,200,300,400,500], 
        'demand':[50,40,30,20,10],
        'stdev':[5,5,5,5,5]
        }


if __name__ == '__main__':

    g = Game(4, fcdata, 100)
    g.run_game()

