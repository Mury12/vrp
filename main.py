import sys
from classes.model.Parser import *
from classes.model.Depot import *

parser = Parser()
parser.parse('CMT', 'CMT7.vrp')
dataset = parser.fileToMatrix('CMT', 'CMT7.vrp')
i = 0

# i = sys.argv[1]
# seed(i)
seed(1)

maxCap = dataset.pop(0)
vehicles = dataset.pop(0)
depotPos = dataset[0]

depot = Depot(
        Point2D(depotPos[0], depotPos[1]),
        vehicles[0],
        maxCap[0]
)

depot.bulk_add_customer(dataset)
depot.trace_routes(0)
depot.show_vehicles()




