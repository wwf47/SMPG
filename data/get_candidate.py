pos = []
typ= {}
#obtain initial candidate types
with open("./seed/actor/positive.txt", "r") as f:
    for line in f.readlines():
        t = line.strip()
        pos.append(t)
with open("./yago/Type-NodeTable.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split("-")
        if t[1] not in typ.keys():
            typ[t[1]] = []
            typ[t[1]].extend(t[0].split(' '))
ts = typ[pos[0]]
seed_com = set(ts)
print(seed_com)
for i in pos:
    t = set(typ[i])
    print(t)
    seed_com = seed_com & t
'''
for n,t in typ.items():
    t = t.split(' ')
    seed_com = seed_com & set(t)'''
types = list(seed_com)
print(types)
print(f"the original length of types: {len(types)}")

#filter the initial candidate types
types = list(seed_com)
concept = {}
typename = []
with open("./yago/NodeType.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split('\t')
        typename.append(t[1])

with open("./yago/concept.txt", "r") as f:
    for line in f.readlines():
        t = line.strip().split('\t')
        if t[1] in typename:
            if (int(typename.index(t[1])+1)) not in concept.keys():
                concept[int(typename.index(t[1])+1)] = []
            if t[0] in typename:
                concept[int(typename.index(t[1])+1)].append(int(typename.index(t[0])+1))

for t in types:
    print(t)
    if int(t) in concept.keys():
        print(True)
        if len(concept[int(t)])>0:
            print(True)
            for j in concept[int(t)]:
                if str(j) in types:
                    types.remove(t)
print(f"the ultimate length of types: {len(types)}")

canout = open("./seed/actor/candidate.txt", "w")
can = []
for n,t in typ.items():
    if types[0] in t:
        can.append(n)
        print(n, sep='', file=canout)









