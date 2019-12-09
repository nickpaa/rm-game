class FareDecrease():
    # decreases fares by 50% (rounds to nearest 100)
    # increases demand by 100%
    
    def __init__(self, game):
        self.name = 'Fare decrease'
        self.message = 'A competitor has lowered fares, and you have decided to match. Fares have gone down, but demand has gone up.'
        self.game = game

    def apply_event(self):
        self.game.fc['fare'] = (self.game.fc['fare'] / 2).round(-2).astype(int)
        self.game.fc['demand'] = (self.game.fc['demand'] * 2).astype(int)


class FareIncrease():
    # increases fares by 50% (rounds to nearest 100)
    # decreases demand by 67%
    
    def __init__(self, game):
        self.name = 'Fare increase'
        self.message = 'You have decided to increase fares to cover increasing costs. Fares have gone up, but demand has gone down.'
        self.game = game

    def apply_event(self):
        self.game.fc['fare'] = (self.game.fc['fare'] * 1.5).round(-2).astype(int)
        self.game.fc['demand'] = (self.game.fc['demand'] * 0.66).astype(int)


class CapacityIncrease():
    # increases capacity by 20 or 50

    def __init__(self, game):
        self.name = 'Capacity increase'
        self.message = 'A larger aircraft has been scheduled on this flight, so capacity has increased.'
        self.game = game

    def apply_event(self):
        if self.game.ac < 100:
            self.game.ac += 20
            self.game.au += 20
        else:
            self.game.ac += 50
            self.game.au += 50
        self.game.sa = self.game.au - self.game.total_lb
        

class CapacityDecrease():
    # decreases capacity by 20 or 50

    def __init__(self, game):
        self.name = 'Capacity decrease'
        self.message = 'A smaller aircraft has been scheduled on this flight, so capacity has decreased.'
        self.game = game

    def apply_event(self):
        if self.game.ac <= 100:
            self.game.ac -= 20
            self.game.au -= 20
        else:
            self.game.ac -= 50
            self.game.au -= 50
        self.game.sa = self.game.au - self.game.total_lb