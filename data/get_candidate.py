pos = []
typ = {}#key is entity index, value is type(in KG)
#obtain entity types of each seed
with open("./seed/actor/positive.txt", "r") as f:
    for line in f.readlines():
        t = line.strip()
        pos.append(t)
#type-entity
with open("./yago/Type-NodeTable.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split("-")
        if t[1] not in typ:
            typ[t[1]] = []
            typ[t[1]].extend(t[0].split(' '))
ts = typ[pos[0]]
seed_com = set(ts)
print(seed_com)
for i in pos:
    t = set(typ[i])
    print(t)
    seed_com = seed_com & t#get seed type

#generate the initial candidates types by the intersection operation
types = list(seed_com)
concept = {}#key is upper class index, value is sub-class index
typename = []
#index-type
with open("./yago/NodeType.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split('\t')
        typename.append(t[1])

with open("./yago/concept.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split('\t')
        if t[1] in typename:
            if (int(typename.index(t[1])+1)) not in concept:
                concept[int(typename.index(t[1])+1)] = []
            if t[0] in typename:
                concept[int(typename.index(t[1])+1)].append(int(typename.index(t[0])+1))

#filter the initial candidates types with the concept hierarchy structure
for t in types:
    if int(t) in concept.keys():
        if len(concept[int(t)])>0:
            for j in concept[int(t)]:
                if str(j) in types:
                    types.remove(t)
print(f"the ultimate length of types: {len(types)}")

#extract candidate entities of satisfying the ultimate candidates types
canout = open("./seed/actor/candidate.txt", "w")
can = []
for e,t in typ.items():
    if types[0] in t:
        can.append(e)
        print(e, sep='', file=canout)










