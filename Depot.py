from Point2D  import *
from Customer import *
from Vehicle  import *

false = False
true  = True

class Depot:
    
    pos = []

    vehicles = []
    customers = []
    _distMatrix = []

    def __init__(self, pos, vehicles, cap):
    
        self.pos = pos
        self.vehicles = self.createVehicles(int(vehicles), int(cap))
    
    def createVehicles(self, amount, cap):
        print("Creating vehicles.. \n")
        vehicles = []
        for i in range (0, amount):
            vehicles.append(Vehicle(i, cap))
        
        print(str(amount)+" Vehicles created.\n")
        return vehicles


    def addCustomer(self, customer):
        self.customers.append(customer)

    def bulkAddCustomer(self, dataset):
        print("Bulk adding customers..\n")
        i = 0;
        for item in dataset:
            pos = Point2D(float(item[0]), float(item[1]))
            demand = int(item[2])
            self.addCustomer(Customer(i, pos, demand))
            i = i+1

        print(str(i)+" Customers added. \n")


    def removeCustomer(self, customer):
        return false

    def traceRoutes(self):
        return false

    def createDistancMatrix(self):
        print("Creating distance matrix..\n")
        d_matrix = []
        i = j = 0
        for customer in self.customers:
            for next_c in self.customers:
                dist = customer.pos.distanceTo(next_c.pos)
                d_matrix.append(dist)

            
            self._distMatrix.append(d_matrix)
        print("Distance matrix created.\n")

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