
import sys
from classes.model.Parser import *
from classes.model.Depot import *
from classes.model.Solver import *
parser = Parser()
# parser.parse()
i=0
sol = []

i = sys.argv[1]

dataset = parser.fileToMatrix(1)


seed(i)

maxCap = dataset.pop(0)
vehicles = dataset.pop(0)
depotPos = dataset[0]

#print(depotPos[0], depotPos[1])

depot = Depot(
        Point2D(depotPos[0], depotPos[1]),
        vehicles[0],
        maxCap[0]
)

depot.bulkAddCustomer(dataset)

# k and refineMethod
# isDone = depot.traceRoutes(1)
# print(depot.vehicles[0].route)
# print(depot.vehicles[1].route)
k = 0 
global_optimal = 99999
best_skip = 0
for k in range (2, dataset.__len__()-1):
    S = Solver(Depot (
            Point2D(depotPos[0], depotPos[1]),
            vehicles[0],
            maxCap[0]
    ), dataset)

    S.traceRoutes(k)
    # print("K = "+str(k)+ ' - '+ str(S.global_optimal))

    if(S.global_optimal < global_optimal):
        best_skip = k
        global_optimal = S.global_optimal

S = Solver(Depot (
            Point2D(depotPos[0], depotPos[1]),
            vehicles[0],
            maxCap[0]
    ), dataset)
S.traceRoutes(best_skip)
#print(str(S.solHeuristic) + ';' + str(S.timeConst*100))
#print(str(S.solRef) + ';' + str((S.timeConst + S.timeRef1) * 100))
#print('Best Skip: '+ str(best_skip))
#print('Best Solution: '+ str(S.global_optimal))
#S.depot.reportLoadedUnloaded()

S._methodGLS()
#print(str(S.solGLS) + ';' + str(S.timeGLS*100))
#print('Best Skip: '+ str(best_skip))
#print('Best Solution: '+ str(S.global_optimal))
#S.depot.reportLoadedUnloaded()
print(str(i) + ';'+ str(S.solHeuristic) + ';' + str(S.timeConst) + ';' + 
str(S.solRef) + ';' + str(S.timeConst + S.timeRef1) + ';' +
str(S.solGLS) + ';' + str(S.timeGLS))