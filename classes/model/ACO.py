from classes.model.Solver import *

false = False
true  = True

class ACO:

    def __init__(self, dataset, max_iteration = 1000):
        self.max_iteration = max_iteration
        self.dataset = dataset
        self.completed = false
        self.solutions = []
        self.pheromon = []
        self.ants = 0

    def _configure(self):

        self.S = Solver(self.dataset)
        
        self.maxCap = self.dataset.pop(0)
        self.vehicles = self.dataset.pop(0)
        self.depotPos = self.dataset[0]

        self.ants = int((int(self.dataset.__len__()) / int(self.vehicles[0]))*1)

        print('Ants used: ' + str(self.ants))


    def _zeroedPheromoneMatrix(self):
        matrix = []
        i = j = 0
        for i in range (0, self.dataset.__len__()):
            v = []
            for j in range (0, self.dataset.__len__()):
                v.append(0)
            matrix.append(v)
        return matrix

    def _updatePheromoneMatrix(self, i, j, add, amount = 0.3):

        if not add:
            self.pheromon[i][j] -= 0.1 if pheromon[i][j] > 0 else 0
            self.pheromon[j][i] -= 0.1 if pheromon[i][j] > 0 else 0
        else:
            self.pheromon[i][j] += amount
            self.pheromon[j][i] += amount
        return;


    def _initialSolution(self, depot,  refinement, skip = 0):
        i=0
        
        depot.bulkAddCustomer(self.dataset)

        for i in range (0, depot._distMatrix[i].__len__()):
            for v in depot.vehicles:
                _next = self._getPheromoneFactorIndex(depot, v.pos, skip)
                if(v.addCustomer(depot.customers[_next[0]], _next[1])):
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
        for i in range (0, self.pheromon[curPos].__len__()):

            _factor = (depot._distMatrix[curPos][i] / self.pheromon[curPos][i]) if self.pheromon[curPos][i] > 0 else depot._distMatrix[curPos][i]
            
            if(_factor < factor and depot._distMatrix[curPos][i] > 0 and depot.customers[i].loaded ):
                    factor = _factor
                    _idx   = i
                    _next  = depot._distMatrix[curPos][i]


        _result = []
        _result.append(_idx)
        _result.append(_next)
        return  _result

    def start(self):
        k=0


        self.pheromon = self._zeroedPheromoneMatrix()
        completed = false

        k = 0
        for j in range (0, self.ants):
            for i in range (0, self.dataset.__len__()):
                depot = self._initialSolution(
                    Depot(
                        Point2D(self.depotPos[0], self.depotPos[1]),
                        self.vehicles[0],self.maxCap[0]),
                        true,
                        0
                    )
                completed = depot.reportLoadedUnloaded()

                # print (i)
                if completed: 
                    sol = []
                    sol.append(depot)
                    sol.append(self.S.global_optimal)
                    self.solutions.append(sol)
                    print(sol[1])
                    break

        # depot.reportLoadedUnloaded(true)
        # for item in self.pheromon:
        #     print (item)

        for item in self.solutions:
            print(item[1])
            # print(item[0].reportLoadedUnloaded(true))

        return

