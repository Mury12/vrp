
import sys
from classes.model.Parser import *
from classes.model.Depot import *
from heuristics.constructive import *

parser = Parser()
parser.parse('CMT', 'CMT1.vrp')
# parser.parse()
i = 0
sol = []

i = sys.argv[1]

dataset = parser.fileToMatrix('CMT', 'CMT1.vrp')

seed(i)
constructive_heuristic(dataset)


'''maxCap = dataset.pop(0)
vehicles = dataset.pop(0)
depotPos = dataset[0]
'''
# print(depotPos[0], depotPos[1])

'''depot = Depot(
        Point2D(depotPos[0], depotPos[1]),
        vehicles[0],
        maxCap[0]
)
'''
# depot.bulk_add_customer(dataset)

# k and refineMethod
# isDone = depot.trace_routes(1)
# print(depot.vehicles[0].route)
# print(depot.vehicles[1].route)

# sol.append(depot.report_loaded_unloaded())
'''
if(not isDone):
    print("There is missing customers. Result needs to be optimized.\n")
    for line in depot._distMatrix:
        print(line)
for v in range(0, depot.vehicles.__len__()):
    print("\nVeículo " + str(v) + str(depot.vehicles[v].route) + '\n')
'''
