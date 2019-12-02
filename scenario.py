from pandas import DataFrame

EASY_FCDATA = {
    'dfd': [4,3,2,1,0],
    'dow_long': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 
    'dow_short': ['Mon','Tue','Wed','Thu','Fri'], 
    'fare':[100,200,300,400,500], 
    'demand':[50,40,30,20,10],
    'stdev':[5,5,5,5,5]
}
EASY_AC = 50

REAL1_FCDATA = {
    'dfd': [4,3,2,1,0],
    'dow_long': ['Monday','Tuesday','Wednesday','Thursday','Friday'], 
    'dow_short': ['Mon','Tue','Wed','Thu','Fri'], 
    'fare':[100,200,300,400,500], 
    'demand':[50,40,30,20,10],
    'stdev':[5,5,5,5,5]
}
REAL1_AC = 100
REAL1_NSRATE = 0.02

REAL2_FCDATA = {
    'dfd': [1,0],
    'dow_long': ['Thursday','Friday'], 
    'dow_short': ['Thu','Fri'], 
    'fare':[400,500], 
    'demand':[20,10],
    'stdev':[5,5]
}
REAL2_AC = 20
REAL2_NSRATE = 0.02

DB_LOW = {'costs':[100,250,500,1000,2000,10000], 'weights':[0.3, 0.4, 0.2, 0.07, 0.03, 0.0001]}
DB_HIGH = {'costs':[100,250,500,1000,2000,10000], 'weights':[0.03, 0.17, 0.45, 0.25, 0.1, 0.01]}


class Scenario():
    
    def __init__(self, sc_dict):
        self.fc = DataFrame(sc_dict['fc']).set_index('dfd')
        self.ndfd = len(self.fc) - 1
        self.ac = sc_dict['ac']


class EasyScenario(Scenario):

    def __init__(self, sc_dict):
        Scenario.__init__(self, sc_dict)


class RealScenario(Scenario):

    def __init__(self, sc_dict):
        Scenario.__init__(self, sc_dict)
        self.ns_rate = sc_dict['ns']
        self.db_costs = sc_dict['db']
        

scenario_dict = {
    0: {'fc':EASY_FCDATA, 'ac':EASY_AC},
    1: {'fc':REAL1_FCDATA, 'ac':REAL1_AC, 'ns':REAL1_NSRATE, 'db':DB_HIGH},
    2: {'fc':REAL2_FCDATA, 'ac':REAL2_AC, 'ns':REAL2_NSRATE, 'db':DB_LOW}
}