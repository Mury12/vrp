from Point2D  import *
from Customer import *
from Vehicle  import *
from random import *
import time
import math

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

        distanceParcial = 0
        for v in self.vehicles:
            distanceParcial += v.getTotalDistance() #soma a distancia percorrido pelo veiculo
            #soma a distancia de volta do veiculo para o depot a partir do ultimo cliente
            distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.pos.x),float(self.pos.y)))
            distanceParcial += distanceVolta
        print("\nDistância total da solução: \n" + str(distanceParcial) + '\n')
        print("Tempo de execução com a heurística construtiva: " + str(self.timeConst) + '\n')
        #se for escolhido usar o método de refinamento de trocas...

        #verifica se existe uma solução para o problema, caso n exista o k é iterado e o programa 
        #buscará por uma nova solução
        #isDone = self.reportLoadedUnloaded()
        #if(not isDone):
        #    self.traceRoutes(k)

        if(ref == 1):
            #print("entrou no refinamento")
            self._changeRefine(4) #alterar aq o envio da optimization rate and seed (seria bom um dps 
            #colocarmos um input())
            distanceParcial = 0
            for v in self.vehicles:
                distanceParcial += v.getTotalDistance() #soma a distancia percorrido pelo veiculo
                #soma a distancia de volta do veiculo para o depot a partir do ultimo cliente 
                distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.pos.x),float(self.pos.y)))
                distanceParcial += distanceVolta
            print("\nNew routes traceds...\n")
            print(self.vehicles)
            print("\nRoutes traced.")
            print("Distância total da solução após refinamento: " + str(distanceParcial) +'\n')
            print("Tempo de execução com a heurística refinamento: " + str(self.timeRef1) +'\n')

        return false
        
    def _getMinorDistanceIndex(self, curPos, k):
        timeStart = time.time()
        _next = 9999
        _idx = 0
        i = 0
        testRow = []
        #altera a posição de um cliente
        #objetivo é alterar a posição um específico cliente caso n encontre uma solução na tentativa anterior
        if(k != 0 and k <self._distMatrix[curPos].__len__()):
            row = []
            row = list(self._distMatrix[curPos])
            val = self._distMatrix[curPos][k]
            row.insert(0, val) #reposiciona o cliente na primeira posição do array
            row.__delitem__(k+1) #remove o cliente da posição q o cliente estava por padrão
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

    def _changeRefine(self, ot):
        timeStart = time.time() #time start do método de refinamento
        i = 0 #Optimization rates = Quantidade de veículos q serão refinados (os veículos q percorrem maior distância)
        _midx = [] #list q armazena o indice real dos veículos em self.vehicles
        _idx = 0 #indice q identifica o veiculo q passou apresentar ter maior distancia percorrida (pior)
        cloneVehicles = self.vehicles
        worstRoutes = [] #list q armazena os piores veiculos
        while i < ot: #para a qtde veiculos q deverá ser refeito
            j = 0
            _next = 0
            for v in cloneVehicles:
                #algoritmo para encontrar o pior veiculo
                if v.distRan > _next:
                    _next = v.distRan
                    _idx = j
                j += 1
            _midx.append(_idx) #registro o indice do pior veiculo encontrado
            worstRoutes.append(cloneVehicles[_idx]) #insere o pior veiculo na lista de piores veiculos
            cloneVehicles[_idx].distRan = 0
            i += 1
        
        for c in worstRoutes:
            for w in range (0,int(c.route.__len__()/2)):
                x = randint(0, c.route.__len__()-1)
                customer1 = c.route[w]
                customer2 = c.route[x]
                c.route.insert(w, customer2)
                c.route.__delitem__(w+1)
                c.route.insert(x, customer1)
                c.route.__delitem__(x+1)
            c.distRan = self._recalcDistanc(c)
        
        sum = 0 #soma da distancia total com o refinamento das piores rotas
        for c in worstRoutes:
            print(c.distRan)
            sum += c.distRan
        
        print("Soma da distância total das rotas que foram refinadas -> " + str(sum))
        for i in range (0,_midx.__len__()):
            self.vehicles[_midx[i]].distRan = worstRoutes[i].distRan #atualiza o distRan da pior rota 
            #self.vehicles.insert(_midx[i], worstRoutes[i])
            #self.vehicles.__delitem__(_midx[i]+1)

        timeEnd = time.time() #calc tempod e execução do método de refinamento
        self.timeRef1 = timeEnd - timeStart

    def _recalcDistanc(self, vec):
        newDistRan = 0 #distancia inicial do recalculo da rota
        for c in range(0, vec.route.__len__() -1 ): #para cada customer da rota - o último
            cActual = str(vec.route[c]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            cNext  = str(vec.route[c+1]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            pointActual = Point2D(float(cActual[0]), float(cActual[1]))
            pointNext = Point2D(float(cNext[0]), float(cNext[1]))
            newDistRan += self.distanceBetween(pointActual, pointNext)
        return newDistRan

    def distanceBetween(self, actual, next): #calcula a distancia entre dois pontos
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
        '''loaded = -1
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
            self.unloaded = false'''

        return self.vehicles
        
