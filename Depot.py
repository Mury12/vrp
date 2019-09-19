from Point2D  import *
from Customer import *
from Vehicle  import *
import random

false = False
true  = True

class Depot:
    
    pos = []

    vehicles = []
    # Usada para calcular as rotas
    customers = []
    # Usada para reservar os clientes
    _customers = []
    _distMatrix = []

    def __init__(self, pos, vehicles, cap):
        
        self.unloaded = false
        self.pos = pos
        self.vehicles = self.createVehicles(int(vehicles), int(cap))
    
    def createVehicles(self, amount, cap):
        print("Creating vehicles.. \n")
        vehicles = []

        for i in range (0, amount):
            vehicles.append(Vehicle(i, cap, self.pos))
        
        print(str(amount)+" Vehicles created.\n")
        return vehicles


    def addCustomer(self, customer):
        self.customers.append(customer)
        self._customers.append(customer)

    def bulkAddCustomer(self, dataset):
        print("Bulk adding customers..\n")
        i = 0
        for item in dataset:
            pos = Point2D(float(item[0]), float(item[1]))
            demand = int(item[2])
            self.addCustomer(Customer(i, pos, demand))
            i = i+1

        print(str(i)+" Customers added. \n")
        self.customers[0].unload()
        self._createDistancMatrix()

    def removeCustomer(self, customer):
        return false

    def traceRoutes(self, k):
        print("Tracing routes..")
        i = 0
        k = k+1
        for i in range (0, self._distMatrix[i].__len__()):
        # for i in range (0, 1):
            for v in self.vehicles:
                _next = self._getMinorDistanceIndex(v.pos,4)
                if(v.addCustomer(self.customers[_next[0]], _next[1])):
                    self.customers[_next[0]].unload()

               
        print(self.vehicles)
        print("Routes traced.")

        # isDone = self.reportLoadedUnloaded()
        # if(not isDone):
        #     self.traceRoutes(k)
        return false
        
        #return false

    def _getMinorDistanceIndex(self, curPos, k):
        _next = 9999
        _idx = 0
        i = 0
        testRow = []
        if(k != 0 and k <self._distMatrix[curPos].__len__()):
            row = []
            row = list(self._distMatrix[curPos])
            val = self._distMatrix[curPos][k]
            row.insert(0, val)
            row.__delitem__(k+1)
            testRow = row
            print("linha" + str(row))
            print("valor " + str(k), "é : " + str(val))
        for d in testRow:
            if(d > 0 and d < _next and self.customers[i].loaded):
                _next = d
                _idx = i
            i += 1

        _result = []
        _result.append(_idx)
        _result.append(_next)
        
        return _result

    def _randomizeResult(self, curPos, seed):
        random.seed(seed)
        _idx = _next = 0
        while((_idx == 0 or _next == -1 or _next == 0) and not self.customers[_idx].loaded):
            _idx = int(random.randint(1, self._distMatrix[_idx].__len__() - 1))
            _next = self._distMatrix[curPos][_idx]

        _result = []
        _result.append(_idx)
        _result.append(_next)

        return _result

    def _createDistancMatrix(self):
        print("Creating distance matrix..\n")
        i = j = 0
        for customer in self.customers:
            d_matrix = []
            for next_c in self.customers:
                dist = customer.pos.distanceTo(next_c.pos)
                d_matrix.append(int(dist))
            
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

    def reportLoadedUnloaded(self):
        loaded = -1
        unloaded = []
        for c in self.customers:
            loaded += 1 if not c.loaded else 0
            if(c.loaded):
                unloaded.append(c)
        
        print(" Unloaded customers: " + str(loaded))
        print(" Total customers: " + str(self.customers.__len__()-1))
        if(unloaded.__len__() > 0):
            print(" Missing customers: ")
            print(unloaded)
            self.unloaded = true
        else:
            self.unloaded = false

        return unloaded.__len__() == 0
        
