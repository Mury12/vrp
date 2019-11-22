# rodar no terminal: python3 main.py seed
# exemplo python3 main.py 10

import sys
from classes.model.Parser import *
from classes.model.Depot import *
from classes.model.Solver import *
from classes.model.ACO import *
parser = Parser()
i=0
sol = []

i = sys.argv[1]
parse = false
if len(sys.argv) == 4 and sys.argv[2] == 'parse':
    # print('parsing file '+ sys.argv[3])
    parser.parse(sys.argv[3])
    # print('file parsed')
    dataset = parser.fileToMatrix(sys.argv[3])
else:
    dataset = parser.fileToMatrix(sys.argv[2])

seed(i)

ants = ACO(dataset, 59)
ants._configure()
reference = time.time()
ants.start()

print(str(ants.dataset.__len__()-1) + ',' + str(ants.ants) + ',' + str(ants.global_optimal[1]) + ',' + str(ants.iterations_used) + ',' + str(time.time() - reference))
