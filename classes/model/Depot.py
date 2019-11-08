from classes.model.Point2D import *
from classes.model.Customer import *
from classes.model.Vehicle import *
from random import *
import time
import math

false = False
true  = True

class Depot:
    
    _customers = []
    timeConst = 0
    timeRef1 = 0

    def __init__(self, pos, vehicles, cap):
        
        self.unloaded = false
        self.pos = pos
        self.vehicles = self.createVehicles(int(vehicles), int(cap))
        self.distMatrix = []
        self.customers = []
        self._distMatrix = []
        self.loaded = 0
    
    def createVehicles(self, amount, cap):
        vehicles = []

        for i in range (0, amount):
            vehicles.append(Vehicle(i, cap, self.pos))
        
        return vehicles


    def addCustomer(self, customer):
        self.customers.append(customer)
        self._customers.append(customer)

    def bulkAddCustomer(self, dataset):
        i = 0
        for item in dataset:
            pos = Point2D(float(item[0]), float(item[1]))
            demand = int(item[2])
            self.addCustomer(Customer(i, pos, demand))
            i = i+1

        self.customers[0].unload()
        self._createDistancMatrix()

    def removeCustomer(self, customer):
        return false

    
    def distanceBetween(self, current, next): #calcula a distancia entre dois pontos
        return math.sqrt( (next.x - current.x) ** 2 + (next.y - current.y) ** 2 )

    def _createDistancMatrix(self):
        #print("Creating distance matrix..\n")
        i = j = 0
        for customer in self.customers:
            d_matrix = []
            for next_c in self.customers:
                dist = customer.pos.distanceTo(next_c.pos)
                d_matrix.append(int(dist))
            
            self._distMatrix.append(d_matrix)
        #print("Distance matrix created.\n")

    def showVehicles(self):
        for truck in self.vehicles:
            print(truck)

    def showCustomers(self):
        for customer in self.customers:
            print(customer)

    def showDistanceMatrix(self):
        for item in self._distMatrix:
            print(item)
            print("\n")

    def reportLoadedUnloaded(self, verb = false):
        loaded = -1
        unloaded = []
        
        if verb:
            for c in self.customers:
                loaded += 1 if not c.loaded else 0
                if(c.loaded):
                    unloaded.append(c)
                print(" Unloaded customers: " + str(loaded))
                print(" Total customers: " + str(self.customers.__len__()-1))
            if(unloaded.__len__() > 0):
                if verb:
                    print(" Missing customers: ")
                    print(unloaded)
                return false
        else:
            return int(self.loaded == self.customers.__len__() - 1)
        
