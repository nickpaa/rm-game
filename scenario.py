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


class Scenario():
    
    def __init__(self, fcdata, ac):
        self.fc = DataFrame(fcdata).set_index('dfd')
        self.ndfd = len(self.fc) - 1
        self.ac = ac


class EasyScenario(Scenario):

    def __init__(self, fcdata, ac):
        Scenario.__init__(self, fcdata, ac)


class RealScenario(Scenario):

    def __init__(self, fcdata, ac, nsrate):
        Scenario.__init__(self, fcdata, ac)
        self.nsrate = nsrate
        


sc_easy = EasyScenario(EASY_FCDATA, EASY_AC)
sc_real1 = RealScenario(REAL1_FCDATA, REAL1_AC, REAL1_NSRATE)

