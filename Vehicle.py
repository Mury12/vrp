from Point2D  import *

class Vehicle:
    
    route = []

    def __init__(self, id, cap):
        self.id = id
        self.cap = cap

    def addCustomer(self, pos):
        self.route.append(pos)
    
    def removeCustomer(self, pos):
        return False

    def __repr__(self):
        return "".join(["Vehicle: ", str(self.id), " - Capacity: ", str(self.cap), "\n"])
