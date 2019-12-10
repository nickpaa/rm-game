from random import choice

DIRECTIONS = ['up','down']

class Event():

    def __init__(self, game):
        self.game = game


class FareChange(Event):

    def __init__(self, game):
        Event.__init__(self, game)

        self.direction = choice(DIRECTIONS)
        
        if self.direction == 'up':
            self.name = 'Fare increase'
            self.message = 'You have decided to increase fares to cover increasing costs. Fares have gone up, but demand has gone down.'    
        elif self.direction == 'down':
            self.name = 'Fare decrease'
            self.message = 'A competitor has lowered fares, and you have decided to match. Fares have gone down, but demand has gone up.'    

        self.image_path = 'images/dollar.png'

    def apply_event(self):
        if self.direction == 'up':
            self.game.fc['fare'] = (self.game.fc['fare'] * 1.5).round(-2).astype(int)
            self.game.fc['demand'] = (self.game.fc['demand'] * 0.66).astype(int).clip(lower=2)
        elif self.direction == 'down':
            self.game.fc['fare'] = (self.game.fc['fare'] / 2).round(-2).astype(int).clip(lower=100)
            self.game.fc['demand'] = (self.game.fc['demand'] * 2).astype(int)


class CapacityChange(Event):

    def __init__(self, game):
        Event.__init__(self, game)
        self.direction = choice(DIRECTIONS)
        
        if self.direction == 'up':
            self.name = 'Capacity increase'
            self.message = 'A larger aircraft has been scheduled on this flight, so capacity has increased.'
        elif self.direction == 'down':
            self.name = 'Capacity decrease'
            self.message = 'A smaller aircraft has been scheduled on this flight, so capacity has decreased.'

        self.image_path = 'images/seat.png'

    def apply_event(self):
        CAP_THRESHOLD = 100
        SMALL_CHANGE = 20
        LARGE_CHANGE = 50

        if self.direction == 'up':
            if self.game.ac < CAP_THRESHOLD:
                self.game.ac += SMALL_CHANGE
                self.game.au += SMALL_CHANGE
            else:
                self.game.ac += LARGE_CHANGE
                self.game.au += LARGE_CHANGE
        
        elif self.direction == 'down':
            if self.game.ac <= CAP_THRESHOLD:
                self.game.ac -= SMALL_CHANGE
                self.game.au -= SMALL_CHANGE
            else:
                self.game.ac -= LARGE_CHANGE
                self.game.au -= LARGE_CHANGE
            
        # update SA to account for new AU
        self.game.sa = self.game.au - self.game.total_lb


class Snowstorm(Event):
    # reduces demand in next two periods

    def __init__(self, game):
        Event.__init__(self, game)

        self.name = 'Snowstorm'
        self.message = 'The forecast calls for heavy snow on Friday, so many people are postponing their travel plans.'
        self.image_path = 'images/snow.png'

    def apply_event(self):
        self.game.fc['demand'] = (self.game.fc['demand'] * 0.2).astype(int).clip(lower=2)  # this is pandas clip, so kw is lower


class Sportsball(Event):

    def __init__(self, game):
        Event.__init__(self, game)

        self.name = 'Sportsball'
        self.message = 'The local sports team has made the playoffs and plays on Friday. There\'s suddenly much more demand, and people are willing to pay more.'
        self.image_path = 'images/sportsball.png'

    def apply_event(self):
        self.game.fc['demand'] = (self.game.fc['demand'] * 3).astype(int).clip(lower=35)
        self.game.fc['fare'] = (self.game.fc['fare'] * 1.5).astype(int)


class Circus(Event):

    def __init__(self, game):
        Event.__init__(self, game)

        self.name = 'Circus'
        self.message = 'The circus is in town. Your leisure demand has gone up a little.'
        self.image_path = 'images/circus.png'

    def apply_event(self):
        self.game.fc.loc[2, 'demand'] = (self.game.fc.loc[2, 'demand'] * 1.5).astype(int).clip(min=8)
        if self.game.curr_dfd == 3:
            self.game.fc.loc[3, 'demand'] = (self.game.fc.loc[3, 'demand'] * 1.5).astype(int).clip(min=8)


class Economy(Event):

    def __init__(self, game):
        Event.__init__(self, game)

        self.direction = choice(DIRECTIONS)
        
        if self.direction == 'up':
            self.name = 'Strong economy'
            self.message = 'Economic trends are improving, so your business demand has gone up.'
            self.image_path = 'images/chartup.png'
        elif self.direction == 'down':
            self.name = 'Weak economy'
            self.message = 'The economy is showing signs of slowing down, and people are reconsidering travel plans. Demand has gone down, and the uncertainty of your forecast has increased.'
            self.image_path = 'images/chartdown.png'
        

    def apply_event(self):
        if self.direction == 'up':
            self.game.fc.loc[0, 'demand'] = (self.game.fc.loc[0, 'demand'] * 2).astype(int).clip(12)
            if self.game.curr_dfd >= 1:
                self.game.fc.loc[1, 'demand'] = (self.game.fc.loc[1, 'demand'] * 1.75).astype(int).clip(17)
            if self.game.curr_dfd >= 2:
                self.game.fc.loc[2, 'demand'] = (self.game.fc.loc[2, 'demand'] * 1.5).astype(int).clip(23)

        elif self.direction == 'down':
            self.game.fc['demand'] = (self.game.fc['demand'] * 0.8).astype(int).clip(2)
            self.game.fc['cv'] = self.game.fc['cv'] * 3
            


if __name__ == '__main__':
    from scenario import scenario_dict, RealScenario
    from game import RealGame
    s = RealScenario(scenario_dict[1])
    g = RealGame(s)
    print(g.fc)
    print(s.events)
    event = Snowstorm(g)
    print(type(event))
    event.apply_event()
    print(g.fc)
    s.redistribute_event_probs(event)
    print(s.events)
    