
import sys
from classes.model.Parser import *
from classes.model.Depot import *
from classes.model.Solver import *
parser = Parser()
i=0
sol = []

i = sys.argv[1]
parse = false
if len(sys.argv) == 3 and sys.argv[2] == 'parse':
    print('parsing file')
    parser.parse()
    print('file parsed')

dataset = parser.fileToMatrix(1)


seed(i)



#print(depotPos[0], depotPos[1])

# k and refineMethod
# isDone = depot.traceRoutes(1)
# print(depot.vehicles[0].route)
# print(depot.vehicles[1].route)

S = Solver(dataset)

S.traceRoutes('gls', true, true)
# print('Best Skip: '+ str(S.best_skip))
print(str(S.global_optimal))
# S.depot.reportLoadedUnloaded(true)

# for s in S.all_solutions:
#     print(s)



# sol.append(depot.reportLoadedUnloaded())
'''
if(not isDone):
    print("There is missing customers. Result needs to be optimized.\n")
    for line in depot._distMatrix:
        print(line)
for v in range(0, depot.vehicles.__len__()):
    print("\nVeículo " + str(v) + str(depot.vehicles[v].route) + '\n')

'''
