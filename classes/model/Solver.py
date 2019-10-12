from classes.model.Depot import *

true = True
false = False

class Solver:

    def __init__(self, depot, dataset):
        
        depot.bulkAddCustomer(dataset)
        self.depot = depot
        self.global_optimal = 9999
        self.current_optimal = self.global_optimal
        self.all_solutions = []

    def traceRoutes(self, skip):
        
        i = 0
        
        for i in range (0, self.depot._distMatrix[i].__len__()):
            for v in self.depot.vehicles:
                _next = self._getMinorDistanceIndex(v.pos, skip)
                if(v.addCustomer(self.depot.customers[_next[0]], _next[1])):
                    self.depot.customers[_next[0]].unload()
                    # self._refine('by change', v.route.__len__()-1)


        distanceParcial = 0
        for v in self.depot.vehicles:
            distanceParcial += v.getTotalDistance() #soma a distancia percorrido pelo veiculo
            #soma a distancia de volta do veiculo para o depot a partir do ultimo cliente
            distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.depot.pos.x),float(self.depot.pos.y)))
            distanceParcial += distanceVolta


        if(1):
            self._refine('by change', 4) #alterar aq o envio da optimization rate and seed (seria bom um dps 
            distanceParcial = 0
            for v in self.depot.vehicles:
                distanceParcial += v.getTotalDistance() #soma a distancia percorrido pelo veiculo
                #soma a distancia de volta do veiculo para o depot a partir do ultimo cliente 
                distanceVolta = v.route[-1][0].pos.distanceTo(Point2D(float(self.depot.pos.x),float(self.depot.pos.y)))
                distanceParcial += distanceVolta

            # print(str(distanceParcial))
            self.all_solutions.append(distanceParcial)
            self.global_optimal = distanceParcial
            #print("Tempo de execução com a heurística refinamento: " + str(self.timeRef1) +'\n')

        return false
        
    def _getMinorDistanceIndex(self, curPos, skip):
        timeStart = time.time()
        _next = 9999
        _idx = 0
        i = 0
        testRow = []
        #altera a posição de um cliente
        #objetivo é alterar a posição um específico cliente caso n encontre uma solução na tentativa anterior
        if(skip != 0 and skip < self.depot._distMatrix[curPos].__len__()):
            row = []
            row = list(self.depot._distMatrix[curPos])
            val = self.depot._distMatrix[curPos][skip]
            row.insert(0, val) #reposiciona o cliente na primeira posição do array
            row.__delitem__(skip+1) #remove o cliente da posição q o cliente estava por padrão
            distance_row = row


        for d in distance_row:
            if(d > 0 and d < _next and self.depot.customers[i].loaded):
                _next = d
                _idx = i
            i += 1

        _result = []
        _result.append(_idx)
        _result.append(_next)

        timeEnd = time.time()
        self.depot.timeConst += timeEnd - timeStart
        
        return _result

    def _refine(self, type, param):
        if type == 'by change':
            self._refine_by_change(param)



    def _refine_by_change(self, routes_to_change):
        timeStart = time.time() #time start do método de refinamento
        i = 0 #Optimization rates = Quantidade de veículos q serão refinados (os veículos q percorrem maior distância)
        _idx = 0 #indice q identifica o veiculo q passou apresentar ter maior distancia percorrida (pior)
        _idx_list = [] #list q armazena o indice real dos veículos em self.vehicles
        cloneVehicles = self.depot.vehicles
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
            c.distRan = self._recalcDistanc(c)
        
        sum = 0 #soma da distancia total com o refinamento das piores rotas
        for c in worstRoutes:
            sum += c.distRan
        
        #print("Soma da distância total das rotas que foram refinadas -> " + str(sum))
        for i in range (0,_idx_list.__len__()):
            self.depot.vehicles[_idx_list[i]].distRan = worstRoutes[i].distRan #atualiza o distRan da pior rota 
            #self.vehicles.insert(_idx_list[i], worstRoutes[i])
            #self.vehicles.__delitem__(_idx_list[i]+1)

        timeEnd = time.time() #calc tempod e execução do método de refinamento
        self.timeRef1 = timeEnd - timeStart

    def _recalcDistanc(self, vec):
        newDistRan = 0 #distancia inicial do recalculo da rota
        for c in range(0, vec.route.__len__() -1 ): #para cada customer da rota - o último
            cActual = str(vec.route[c]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            cNext  = str(vec.route[c+1]).split('(')[1].split(')')[0].split(',') #obter os pontos do customer
            pointActual = Point2D(float(cActual[0]), float(cActual[1]))
            pointNext = Point2D(float(cNext[0]), float(cNext[1]))
            newDistRan += self.depot.distanceBetween(pointActual, pointNext)
        return newDistRan



    