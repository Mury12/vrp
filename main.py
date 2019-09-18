from Parser import *
from Depot import *

parser = Parser()

dataset = parser.fileToMatrix(1)


maxCap = dataset.pop(0)
vehicles = dataset.pop(0)
depotPos = dataset.pop(0)

print(depotPos[0], depotPos[1])

depot = Depot(
            Point2D(depotPos[0], depotPos[1]),
            vehicles[0],
            maxCap[0]
        )
depot.bulkAddCustomer(dataset)
depot.createDistancMatrix()
print(depot._distMatrix[0].__len__())