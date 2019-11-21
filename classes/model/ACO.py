from classes.model.Solver import *
import copy

false = False
true  = True

class ACO:

    def __init__(self, dataset, max_iteration = 1000):
        self.max_iteration = max_iteration
        self.not_improved = int(max_iteration/10) if max_iteration > 100 else 10
        self.iterations_used = 0
        self.dataset = dataset
        self.completed = false
        self.solutions = []
        self.pheromon = []
        self.updated_pheromon = []
        self.ants = 0
        self.global_optimal = 0

    def _configure(self):

        self.S = Solver(self.dataset)
        self.maxCap = self.dataset.pop(0)
        self.vehicles = self.dataset.pop(0)
        self.depotPos = self.dataset[0]

        self.pheromon = self._zeroedPheromoneMatrix()        
        self.updated_pheromon = self._zeroedPheromoneMatrix()        
        self.ants = int(self.vehicles[0])*2

        # print('Ants used: ' + str(self.ants))


    def _zeroedPheromoneMatrix(self):
        matrix = []
        i = j = 0
        for i in range (0, self.dataset.__len__()):
            v = []
            for j in range (0, self.dataset.__len__()):
                v.append(0)
            matrix.append(v)
        return matrix

    def _updatePheromoneMatrix(self, i, j, add, amount = 0.5):

        if not add:
            for i in range (0, self.updated_pheromon.__len__() - 1):
                for j in range (0, self.updated_pheromon[i].__len__() - 1):
                    if self.updated_pheromon[i][j] > 0.2:
                        self.updated_pheromon[i][j] -= 0.2
                    else: self.updated_pheromon[i][j] = 0
        else:
            if(self.updated_pheromon[i][j] > 0):
                self.updated_pheromon[i][j] += amount/2
                self.updated_pheromon[j][i] += amount/2
            else:
                self.updated_pheromon[i][j] += amount
                self.updated_pheromon[j][i] += amount
        return;


    def run(self, depot,  refinement, skip = 0):
        i=0
        
        depot.bulkAddCustomer(self.dataset)

        for i in range (skip, depot._distMatrix[i].__len__() - 1):
            for v in depot.vehicles:
                _next = self._getPheromoneFactorIndex(depot, v.pos, skip)
                if(_next and v.addCustomer(depot.customers[_next[0]], _next[1])):
                    depot.customers[_next[0]].unload()
                    depot.loaded += 1
                    self._updatePheromoneMatrix(i, v.pos, true)
        
        depot = self.S._updateRouteTotalDistance(depot)

        return depot


    def _getPheromoneFactorIndex(self, depot, curPos, skip = 0):
        factor = 99999
        _idx = 0
        _next = 9999
        _skipped = 0;

        _pheromon_row = list(self.pheromon[curPos])
        _distance_row = list(depot._distMatrix[curPos])
        _pheromon_row.insert(0, _pheromon_row.pop(skip))
        _distance_row.insert(0, _distance_row.pop(skip))

        for i in range (0, _pheromon_row.__len__()):
            
            _factor = (_distance_row[i] - _pheromon_row[i]) 

            if(_factor < factor and depot.customers[i].loaded and _distance_row[i] > 0):
                factor = _factor
                _idx   = i
                _next  = _distance_row[i]

        _result = []
        _result.append(_idx)
        _result.append(_next)
        if _next == 9999: _result = false
        return  _result

    def _releaseAntColony(self):
        for j in range (0, self.ants):
            for i in range (j if j < self.dataset.__len__() else 0, self.dataset.__len__()):
                depot = self.run(
                    Depot(
                        Point2D(self.depotPos[0], self.depotPos[1]),
                        self.vehicles[0],self.maxCap[0]),
                        true,
                        randint(0, self.dataset.__len__() - 5)
                    )
                completed = depot.reportLoadedUnloaded()

                # print (i)
                if completed:
                    sol = []
                    sol.append(depot)
                    sol.append(self.S.global_optimal)
                    self.solutions.append(sol)
                    if sol[1] < self.solutions[self.global_optimal][1]:
                        self.global_optimal = self.solutions.__len__() - 1
                        # print(sol[1])

                    break


        self._updatePheromoneMatrix(0,0,false)
        self.pheromon = copy.deepcopy(self.updated_pheromon)

    def start(self):

        for k in range (0, self.max_iteration):
            
            self._releaseAntColony()
            
        self.global_optimal = self.solutions[self.global_optimal]

        return

