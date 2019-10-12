from classes.model.Point2D import *
from classes.model.Customer import *


class Vehicle:

    def __init__(self, id, cap, curPos):
        self.id = id
        self.cap = cap
        self.pos = 0
        self.usedCap = 0
        self.distRan = 0
        self.route = []

    def addCustomer(self, customer, distance):
        if customer.loaded:
            if (self.usedCap + customer.demand) <= self.cap:
                self.usedCap += customer.demand
                route = []
                route.append(customer)
                route.append(distance)
                self.route.append(route)
                self.pos = customer.id
                self.distRan += distance
                return True
        return False
    
    def removeCustomer(self, idxCustomer):
        self.route.__delitem__(idxCustomer)
        # return False

    def getTotalDistance(self):
        total = 0

        for item in self.route:
            total += item[1]
        
        return total

    def get_route(self):
        return self.route

    def __repr__(self):
        return "".join(["Vehicle: ", str(self.id), " - Capacity: ", str(self.cap), " - Used cap: ", str(self.usedCap),
                        " - Distance ran: ", str(self.distRan), " - Last customer: ", str(self.route[-1]), "\n"])
