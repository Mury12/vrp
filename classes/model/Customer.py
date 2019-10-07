from classes.model.Point2D  import *

class Customer:

    def __init__(self, id, pos, demand):
        self.pos = pos
        self.demand = demand
        self.id = id
        self.loaded = True

    def getDemand(self):
        return self.demand

    def unload(self):
        self.loaded = False

    def load(self):
        self.loaded = True
        
    def getPosition(self):
        return self.pos

    def __repr__(self):
        return "".join(["Customer ", str(self.id), ": ", str(self.pos), ", Demand: ", str(self.demand)])