from Point2D  import *
from Customer import *
from Vehicle  import *
import random
import time

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
    timeConst = 0
    timeRef1 = 0
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

    def traceRoutes(self, ref):
        print("Tracing routes..")
        i = 0
        #k = k if k > 0 else k + 1
        for i in range (0, self._distMatrix[i].__len__()):
        # for i in range (0, 1):
            for v in self.vehicles:
                _next = self._getMinorDistanceIndex(v.pos,4)
                if(v.addCustomer(self.customers[_next[0]], _next[1])):
                    self.customers[_next[0]].unload()

               
        print(self.vehicles)
        print("Routes traced.\n")

        i = 0
        distanceParcial = 0
        for v in self.vehicles:
            #print("Vehicle: " + str(i) + str(v.route))
            #distancia percorrida pelo veiculo na rota obs.: sem contar a volta ao depot
            distanceParcial += v.getTotalDistance()
            #print("rota " + str(i) + " distancia: " + str(distanceParcial))
            #obtem distancia para voltar ao depot
            distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.pos.x),float(self.pos.y)))
            #print("Distancia de volta " + str(distanceVolta))
            #acrescenta a distancia de volta à distância percorrida pelo veículo v (que resulta na 
            # distancia total da solução)
            distanceParcial += distanceVolta
            #i = i + 1
        print("\nDistância total da solução: \n" + str(distanceParcial) + '\n')
        print("Tempo de execução com a heurística construtiva: " + str(self.timeConst) + '\n')
        #se for escolhido usar o método de refinamento de trocas...
        if(ref == 1):
            #print("entrou no refinamento")
            self._changeRefine()
            distanceParcial = 0
            for v in self.vehicles:
                #print("Vehicle: " + str(i) + str(v.route))
                #distancia percorrida pelo veiculo na rota obs.: sem contar a volta ao depot
                distanceParcial += v.getTotalDistance()
                #print("rota " + str(i) + " distancia: " + str(distanceParcial))
                #obtem distancia para voltar ao depot
                distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.pos.x),float(self.pos.y)))
                #print("Distancia de volta " + str(distanceVolta))
                #acrescenta a distancia de volta à distância percorrida pelo veículo v (que resulta na 
                # distancia total da solução)
                distanceParcial += distanceVolta
                #i = i + 1
            print("\nNew routes traceds...\n")
            print(self.vehicles)
            print("\nRoutes traced.")
            print("Distância total da solução após refinamento: " + str(distanceParcial) +'\n')
            print("Tempo de execução com a heurística refinamento: " + str(self.timeRef1) +'\n')

            

        #isDone = self.reportLoadedUnloaded()
        #if(not isDone):
        #    self.traceRoutes(k)
        return false
        
        #return false

    def _getMinorDistanceIndex(self, curPos, k):
        timeStart = time.time()
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
            #print("linha" + str(row))
            #print("valor " + str(k), "é : " + str(val))
        for d in testRow:
            if(d > 0 and d < _next and self.customers[i].loaded):
                _next = d
                _idx = i
            i += 1

        _result = []
        _result.append(_idx)
        _result.append(_next)

        timeEnd = time.time()
        self.timeConst += timeEnd - timeStart
        
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

    def _changeRefine(self):
        timeStart = time.time()
        i = 0
        _midx = []
        _idx = 0
        cloneVehicles = self.vehicles
        worstRoutes = []
        ans = []
        while i < 8:
            j = 0
            _next = 0
            for v in cloneVehicles:
                if v.distRan > _next:
                    _next = v.distRan
                    _idx = j
                j += 1
            _midx.append(_idx)
            worstRoutes.append(cloneVehicles[_idx])
            cloneVehicles[_idx].distRan = 0
            #cloneVehicles.__delitem__(_idx)
            #print("pior rota: " + str(worstRoutes))
            i += 1
        #print("valor antigo da rota 0: " + str(worstRoutes[0].distRan))
        for c in worstRoutes:
            for w in range (0,int(c.route.__len__()/2)):
                #print("entrada route  " + str(c.route))
                customer1 = c.route[w]
                customer2 = c.route[w%(c.route.__len__()-1)]
                c.route.insert(w, customer2)
                c.route.__delitem__(w+1)
                c.route.insert(w%3, customer1)
                c.route.__delitem__((w%c.route.__len__()-1) + 1)
            #print("saida route : " + str(c.route))
            ans = self._recalcDistanc(c)
            c.distRan = ans
        
        sum = 0
        for c in worstRoutes:
            print(c.distRan)
            sum += c.distRan
        
        print("Soma da distância total das rotas que foram refinadas -> " + str(sum))
        for i in range (0,_midx.__len__()):
            self.vehicles.insert(_midx[i], worstRoutes[i])
            self.vehicles.__delitem__(_midx[i]+1)

        timeEnd = time.time()
        self.timeRef1 = timeEnd - timeStart
        # print("valor novo da distRan 0: " + str(worstRoutes[0].distRan))
        # print("valor novo da distRan 1: " + str(worstRoutes[1].distRan))
        # worstRoutes[0].removeCustomer(0)
        #print(worstRoutes[0].route)

        
    def _recalcDistanc(self, vec):
        newDistRan = 0
        for c in range(0, vec.route.__len__() -1 ):
            if c <= (vec.route.__len__()):
                cActual = str(vec.route[c]).split('(')[1].split(')')[0].split(',')
                cNext  = str(vec.route[c+1]).split('(')[1].split(')')[0].split(',')
                pointActual = Point2D(float(cActual[0]), float(cActual[1]))
                pointNext = Point2D(float(cNext[0]), float(cNext[1]))
                #print(pointNext)
                newDistRan += self.distanceBetween(pointActual, pointNext)
        #print("distancia da nova rota: " + str(newDistRan))
        return newDistRan

    def distanceBetween(self, actual, next):
        return math.sqrt( (next.x - actual.x) ** 2 + (next.y - actual.y) ** 2 )

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
        
