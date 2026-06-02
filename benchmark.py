import timeit
import random

def current_way(speciesList):
    tmp = {x[0]: set([]) for x in speciesList}
    tmp2 = {x[0]: set([]) for x in speciesList}
    tmp3 = {x[0]: set([]) for x in speciesList}
    tmp4 = {x[0]: set([]) for x in speciesList}
    for x in speciesList:
        if x[3] in ["BQB_IS", "BQM_IS", "BQB_IS_VERSION_OF"]:
            tmp[x[0]].add(x[1])
            if x[2] != "":
                tmp2[x[0]].add(x[2])
            tmp3[x[0]].add(x[3])
        else:
            tmp4[x[0]].add((x[1], x[3]))
    return tmp, tmp2, tmp3, tmp4

def new_way(speciesList):
    tmp = {}
    tmp2 = {}
    tmp3 = {}
    tmp4 = {}
    for x in speciesList:
        key = x[0]
        if key not in tmp:
            tmp[key] = set()
            tmp2[key] = set()
            tmp3[key] = set()
            tmp4[key] = set()

        if x[3] in ('BQB_IS', 'BQM_IS', 'BQB_IS_VERSION_OF'):
            tmp[key].add(x[1])
            if x[2] != '':
                tmp2[key].add(x[2])
            tmp3[key].add(x[3])
        else:
            tmp4[key].add((x[1], x[3]))
    return tmp, tmp2, tmp3, tmp4

speciesList = [(f'species_{random.randint(0, 100)}', f'uri_{i}', f'name_{i}', random.choice(['BQB_IS', 'BQM_IS', 'BQB_IS_VERSION_OF', 'OTHER'])) for i in range(1000)]

print('Current:', timeit.timeit(lambda: current_way(speciesList), number=10000))
print('New:', timeit.timeit(lambda: new_way(speciesList), number=10000))
