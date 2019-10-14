from classes.model.Depot import *

true = True
false = False

class Solver:

    def __init__(self, dataset):
        
        self.dataset = dataset
        self.global_optimal = 9999
        self.current_optimal = self.global_optimal
        self.all_solutions = []
        self.completed = false
        self.best_skip = 0

    def traceRoutes(self, method, refinement = false, choose_best_skip = false):
        
        if method == 'gls':
            depot = self._guidedLocalSearch(choose_best_skip, refinement)

        self.completed = depot.reportLoadedUnloaded()
        
        return false
        

    def _initialSolution(self, depot,  refinement, skip = 0):
        i=0
        
        depot.bulkAddCustomer(self.dataset)

        for i in range (0, depot._distMatrix[i].__len__()):
            for v in depot.vehicles:
                _next = self._getMinorDistanceIndex(depot, v.pos, skip)
                if(v.addCustomer(depot.customers[_next[0]], _next[1])):
                    depot.customers[_next[0]].unload()

        depot = self._updateRouteTotalDistance(depot)

        if(refinement):
            depot = self._refine(depot, 'by change', 4)

        self.completed = depot.reportLoadedUnloaded()

        return depot


    def _updateRouteTotalDistance(self, depot):
        partialDistance = 0
        for v in depot.vehicles:
            partialDistance += v.getTotalDistance() #soma a distancia percorrido pelo veiculo
            #soma a distancia de volta do veiculo para o depot a partir do ultimo cliente
            returnDistance = v.route[-1][0].pos.distanceTo(Point2D(float(depot.pos.x),float(depot.pos.y)))
            partialDistance += returnDistance
                       
            self.global_optimal = partialDistance
        return depot

    def _guidedLocalSearch(self, choose_best_skip = false, refinement = false):

        

        if not choose_best_skip:
            maxCap = self.dataset.pop(0)
            vehicles = self.dataset.pop(0)
            depotPos = self.dataset[0]
            depot = self._initialSolution(
                Depot(
                    Point2D(depotPos[0], depotPos[1]),
                    vehicles[0],maxCap[0]),
                    refinement,
                    i
                ) 
            self.all_solutions.append(self.global_optimal)
        else:
            depot = self._chooseBestSkipSolution(refinement)

        depot.reportLoadedUnloaded(true)
        return depot

        #print("Tempo de execução com a heurística refinamento: " + str(self.timeRef1) +'\n')

    def _calculatePenalties(self, routeIdx):
        return false

    def _chooseBestSkipSolution(self, refinement = false):
        i = 0
        global_optimal = 999999
        best_skip = 0
        best_depot = ''
        
        maxCap = self.dataset.pop(0)
        vehicles = self.dataset.pop(0)
        depotPos = self.dataset[0]

        for i in range (2, self.dataset.__len__() - 1):
            depot = self._initialSolution(
                Depot(
                    Point2D(depotPos[0], depotPos[1]),
                    vehicles[0],maxCap[0]),
                    refinement,
                    i
                )
            if self.global_optimal < global_optimal and self.completed:
                best_skip = i
                global_optimal = self.global_optimal
                best_depot = depot
                self.all_solutions.append(global_optimal)
            # print(global_optimal)
        
        self.best_skip = best_skip
        self.global_optimal = global_optimal

        return best_depot

    def _getMinorDistanceIndex(self, depot, curPos, skip):
        skip = skip if skip > 0 else 1
        timeStart = time.time()
        _next = 9999
        _idx = 0
        i = 0
        testRow = []
        #altera a posição de um cliente
        #objetivo é alterar a posição um específico cliente caso n encontre uma solução na tentativa anterior
        
        distance_row = []
        if(skip != 0 and skip < depot._distMatrix[curPos].__len__()):
            row = []
            row = list(depot._distMatrix[curPos])
            val = depot._distMatrix[curPos][skip]
            row.insert(0, val) #reposiciona o cliente na primeira posição do array
            row.__delitem__(skip+1) #remove o cliente da posição q o cliente estava por padrão
            distance_row = row

        for d in distance_row:
            if(d > 0 and d < _next and depot.customers[i].loaded):
                _next = d
                _idx = i
            i += 1

        _result = []
        _result.append(_idx)
        _result.append(_next)

        timeEnd = time.time()
        depot.timeConst += timeEnd - timeStart
        
        return _result

    def _refine(self, depot, type, param):

        if type == 'by change':
            self._refine_by_change(depot, param)

        depot = self._updateRouteTotalDistance(depot)
        return depot



    def _refine_by_change(self, depot, routes_to_change):
        timeStart = time.time() #time start do método de refinamento
        i = 0 #Optimization rates = Quantidade de veículos q serão refinados (os veículos q percorrem maior distância)
        _idx = 0 #indice q identifica o veiculo q passou apresentar ter maior distancia percorrida (pior)
        _idx_list = [] #list q armazena o indice real dos veículos em self.vehicles
        cloneVehicles = depot.vehicles
        worstRoutes = [] #list q armazena as piores rotas

        while i < routes_to_change: #para a qtde veiculos q deverá ser refeito
            j = 0
            _next = 0
            for v in cloneVehicles:
                #algoritmo para encontrar o pior veiculo
                if v.distRan > _next:
                    _next = v.distRan
                    _idx = j
                j += 1

            _idx_list.append(_idx) #registro o indice do pior veiculo encontrado
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
            c.distRan = self._rebuildDistances(depot, c)
        
        sum = 0 #soma da distancia total com o refinamento das piores rotas
        for c in worstRoutes:
            sum += c.distRan
        
        #print("Soma da distância total das rotas que foram refinadas -> " + str(sum))
        for i in range (0,_idx_list.__len__()):
            depot.vehicles[_idx_list[i]].distRan = worstRoutes[i].distRan #atualiza o distRan da pior rota 
            #self.vehicles.insert(_idx_list[i], worstRoutes[i])
            #self.vehicles.__delitem__(_idx_list[i]+1)

        timeEnd = time.time() #calc tempod e execução do método de refinamento
        self.timeRef1 = timeEnd - timeStart

        return depot

    def _rebuildDistances(self, depot, vec):
        newDistRan = 0 #distancia inicial do recalculo da rota
        for c in range(0, vec.route.__len__() -1 ): #para cada customer da rota - o último
            cActual = str(vec.route[c]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            cNext  = str(vec.route[c+1]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            pointActual = Point2D(float(cActual[0]), float(cActual[1]))
            pointNext = Point2D(float(cNext[0]), float(cNext[1]))
            newDistRan += depot.distanceBetween(pointActual, pointNext)
        return newDistRan



    