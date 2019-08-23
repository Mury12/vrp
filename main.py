import re

i = 0
rows = []
node_section = False
demand_section = False
depot_section = False
for i in range(1, 2):
    f = open('plain/fixed'+str(i)+'.txt', 'r')
    for line in f:
        if(re.findall(r"NODE_COORD_SECTION", line)):
            node_section = True
            continue
        if(re.findall(r"DEMAND_SECTION", line)):
            node_section = False
            demand_section = True
            continue
        if(re.findall(r"DEPOT_SECTION", line)):
            demand_section = False
            depot_section = True
            continue

        if(re.findall(r"CAPACITY", line) 
        or re.findall(r"DISTANCE", line)
        or re.findall(r"VEHICLES", line)):
            _f = open('plain/ready/fixed'+str(i)+'.txt', 'a')
            _f.write(line)
            _f.close()
        
        if(node_section):
            row = line.split()
            row.pop(0)
            rows.append(row)
        
        if(demand_section):
            row = line.split()
            idx = row[0]
            row.pop(0)
            #print(row)
            rows[int(idx)-1].append(row[0])
        if(depot_section):
            _f = open('plain/ready/fixed'+str(i)+'.txt', 'a')
            depot = line.split()
            depot.append(0)
            _f.write(" ".join(str(el) for el in depot) + '\n')
            _f.close()
            break
    for row in rows:
        _f = open('plain/ready/fixed'+str(i)+'.txt', 'a')
        _f.write(" ".join(str(el) for el in row) + '\n')
        _f.close()   

    f.close()