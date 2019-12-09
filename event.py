from random import choice

DIRECTIONS = ['up','down']

class FareChange():

    def __init__(self, game):
        self.direction = choice(DIRECTIONS)
        
        if self.direction == 'up':
            self.name = 'Fare increase'
            self.message = 'You have decided to increase fares to cover increasing costs. Fares have gone up, but demand has gone down.'    
        elif self.direction == 'down':
            self.name = 'Fare decrease'
            self.message = 'A competitor has lowered fares, and you have decided to match. Fares have gone down, but demand has gone up.'    

        self.image_path = 'images/dollar.png'

        self.game = game

    def apply_event(self):
        if self.direction == 'up':
            self.game.fc['fare'] = (self.game.fc['fare'] * 1.5).round(-2).astype(int)
            # self.game.fc['demand'] = max((self.game.fc['demand'] * 0.66).astype(int), 2)
            self.game.fc['demand'] = (self.game.fc['demand'] * 0.66).astype(int)
        elif self.direction == 'down':
            # self.game.fc['fare'] = max((self.game.fc['fare'] / 2).round(-2).astype(int), 100)
            self.game.fc['fare'] = (self.game.fc['fare'] / 2).round(-2).astype(int)
            self.game.fc['demand'] = (self.game.fc['demand'] * 2).astype(int)


# class FareDecrease():
#     # decreases fares by 50% (rounds to nearest 100)
#     # increases demand by 100%
    
#     def __init__(self, game):
#         self.name = 'Fare decrease'
#         self.message = 'A competitor has lowered fares, and you have decided to match. Fares have gone down, but demand has gone up.'
#         self.image_path = 'images/dollar.png'
#         self.game = game

#     def apply_event(self):
#         self.game.fc['fare'] = (self.game.fc['fare'] / 2).round(-2).astype(int)
#         self.game.fc['demand'] = (self.game.fc['demand'] * 2).astype(int)


# class FareIncrease():
#     # increases fares by 50% (rounds to nearest 100)
#     # decreases demand by 67%
    
#     def __init__(self, game):
#         self.name = 'Fare increase'
#         self.message = 'You have decided to increase fares to cover increasing costs. Fares have gone up, but demand has gone down.'
#         self.image_path = 'images/dollar.png'
#         self.game = game

#     def apply_event(self):
#         self.game.fc['fare'] = (self.game.fc['fare'] * 1.5).round(-2).astype(int)
#         self.game.fc['demand'] = (self.game.fc['demand'] * 0.66).astype(int)


class CapacityChange():

    def __init__(self, game):
        self.direction = choice(DIRECTIONS)
        
        if self.direction == 'up':
            self.name = 'Capacity increase'
            self.message = 'A larger aircraft has been scheduled on this flight, so capacity has increased.'
        elif self.direction == 'down':
            self.name = 'Capacity decrease'
            self.message = 'A smaller aircraft has been scheduled on this flight, so capacity has decreased.'

        self.image_path = 'images/seat.png'

        self.game = game

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


# class CapacityIncrease():
#     # increases capacity by 20 or 50

#     def __init__(self, game):
#         self.name = 'Capacity increase'
#         self.message = 'A larger aircraft has been scheduled on this flight, so capacity has increased.'
#         self.image_path = 'images/seat.png'
#         self.game = game

#     def apply_event(self):
#         if self.game.ac < 100:
#             self.game.ac += 20
#             self.game.au += 20
#         else:
#             self.game.ac += 50
#             self.game.au += 50
#         self.game.sa = self.game.au - self.game.total_lb
        

# class CapacityDecrease():
#     # decreases capacity by 20 or 50

#     def __init__(self, game):
#         self.name = 'Capacity decrease'
#         self.message = 'A smaller aircraft has been scheduled on this flight, so capacity has decreased.'
#         self.image_path = 'images/seat.png'
#         self.game = game

#     def apply_event(self):
#         if self.game.ac <= 100:
#             self.game.ac -= 20
#             self.game.au -= 20
#         else:
#             self.game.ac -= 50
#             self.game.au -= 50
#         self.game.sa = self.game.au - self.game.total_lb


class Snowstorm():
    # reduces demand in next two periods

    def __init__(self, game):
        self.name = 'Snowstorm'
        self.message = 'The forecast calls for heavy snow on Friday, so many people are postponing their travel plans.'
        self.image_path = 'images/snow.png'
        self.game = game

    def apply_event(self):
        self.game.fc['demand'] = (self.game.fc['demand'] * 0.2).astype(int).clip(lower=2)  # this is pandas clip, so kw is lower
