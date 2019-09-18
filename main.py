from Parser import *
from Depot import *

parser = Parser()
# parser.parse()
dataset = parser.fileToMatrix(1)


maxCap = dataset.pop(0)
vehicles = dataset.pop(0)
depotPos = dataset[0]

print(depotPos[0], depotPos[1])

depot = Depot(
            Point2D(depotPos[0], depotPos[1]),
            vehicles[0],
            maxCap[0]
        )
depot.bulkAddCustomer(dataset)

depot.traceRoutes()
# print(depot.vehicles[0].route)
# print(depot.vehicles[1].route)

isDone = depot.reportLoadedUnloaded()

if(not isDone):
    print("There is missing customers. Result needs to be optimized.\n")
# for line in depot._distMatrix:
#     print(line)

