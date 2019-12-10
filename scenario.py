from pandas import DataFrame
from event import *

MF_DOW_LONG = ['Monday','Tuesday','Wednesday','Thursday','Friday']
MF_DOW_SHORT = ['Mon','Tue','Wed','Thu','Fri']

EASY_FCDATA = {
    'dfd': [3,2,1,0],
    'dow_long': MF_DOW_LONG[1:], 
    'dow_short': MF_DOW_SHORT[1:], 
    'fare':[100,200,300,400], 
    'demand':[80,60,40,20],
    'cv':[0,0,0,0]
}
EASY_AC = 100

# EASY_FCDATA = {
#     'dfd': [1,0],
#     'dow_long': MF_DOW_LONG[-2:], 
#     'dow_short': MF_DOW_SHORT[-2:], 
#     'fare':[400,500], 
#     'demand':[20,10],
#     'cv':[0,0]
# }
# EASY_AC = 50

REAL1_FCDATA = {
    'dfd': [4,3,2,1,0],
    'dow_long': MF_DOW_LONG, 
    'dow_short': MF_DOW_SHORT, 
    'fare':[100,200,300,400,500], 
    'demand':[50,40,30,20,10],
    'cv':[0.05,0.1,0.15,0.2,0.25]
}
REAL1_AC = 100
REAL1_NSRATE = 0.02

REAL2_FCDATA = {
    'dfd': [4,3,2,1,0],
    'dow_long': MF_DOW_LONG, 
    'dow_short': MF_DOW_SHORT, 
    'fare':[200,300,400,500,600], 
    'demand':[80,60,40,30,20],
    'cv':[0.1,0.2,0.3,0.4,0.5]
}
REAL2_AC = 180
REAL2_NSRATE = 0.04

DB_LOW = {'costs':[100,250,500,1000,2000,5000,10000], 'weights':[0.3, 0.4, 0.2, 0.07, 0.03, 0.01, 0.0001]}
DB_MEDIUM = {'costs':[100,250,500,1000,2000,5000,10000], 'weights':[0.15, 0.25, 0.35, 0.25, 0.03, 0.02, 0.001]}
DB_HIGH = {'costs':[100,250,500,1000,2000,5000,10000], 'weights':[0.05, 0.15, 0.25, 0.45, 0.1, 0.05, 0.05]}

scenario_dict = {
    0: {'name':'Easy mode', 'image':'images/100.png', 'fc':EASY_FCDATA, 'ac':EASY_AC},
    1: {'name':'SFO', 'image':'images/bridge.png', 'fc':REAL1_FCDATA, 'ac':REAL1_AC, 'ns':REAL1_NSRATE, 'db':DB_MEDIUM,
        'events':[FareChange] * 15 + [CapacityChange] * 10 + [Economy] * 20 + [Sportsball] * 15 + [None] * 40},
    2: {'name':'IAH', 'image':'images/oil.png', 'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW,
        'events':[FareChange] * 20 + [CapacityChange] * 10 + [Circus] * 10 + [Snowstorm] * 5 + [None] * 55},
    3: {'name':'NRT', 'image':'images/cherry.png', 'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW},
    4: {'name':'FCO', 'image':'images/fountain.png', 'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW},
    5: {'name':'HNL', 'image':'images/beach.png', 'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW},
    6: {'name':'SJO', 'image':'images/outdoors.png', 'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW}
}


class Scenario():
    
    def __init__(self, sc_dict):
        self.name = sc_dict['name']
        self.fc = DataFrame(sc_dict['fc']).set_index('dfd')
        self.fc['stdev'] = self.fc['demand'] * self.fc['cv']
        self.ndfd = len(self.fc) - 1
        self.ac = sc_dict['ac']
        self.image_path = sc_dict['image']


class EasyScenario(Scenario):

    def __init__(self, sc_dict):
        Scenario.__init__(self, sc_dict)


class RealScenario(Scenario):

    def __init__(self, sc_dict):
        Scenario.__init__(self, sc_dict)
        self.ns_rate = sc_dict['ns']
        self.db_costs = sc_dict['db']
        self.events = sc_dict['events']
        
        