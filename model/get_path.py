import time
import collections

def findpath(seed, node, value, x):
    node_rel1 = {}#key is nid, value is rel dict
    node_rel2 = {}#key is nid, value is relation path
    rel1 = []
    rel2 = []
    link = {}#key is nodeid,
    path = {}#key is path, value is number of seed pair
    time0 = time.time()
    for i in seed:
        link[int(i)] = {}
        node_rel1[int(i)] = node[int(i)]
        print("the link related to node is: "+str(len(node[int(i)])))
        for j in node[int(i)]:#get relid(dictk)
            rel1.append(j)
            for k in node[int(i)][j]:#get target nid(list)
                for m in node[int(k)]:#get relid
                    #add relation
                    if j+'_'+m not in link[int(i)]:
                        rel2.append(j+'_'+m)
                        link[int(i)][j+'_'+m] = []
                    link[int(i)][j+'_'+m] = link[int(i)][j+'_'+m]+node[int(k)][m]#get next relation related nodes
        node_rel2[int(i)] = link[int(i)]
        print('the dictionary of relation with length 2 has been built,the number is:')
    for s in seed:
        print(len(link[int(s)]))

    #record the seed count of each 1-relation contains
    d1 = collections.Counter(rel1)
    rel1_num = dict(d1)
    d2 = collections.Counter(rel2)
    rel2_num = dict(d2)

    print("origin: the number of relation with length 1:"+str(len(node_rel1)))
    print("origin: the number of relation with length 2:"+str(len(node_rel2)))

    #maximum number of source set
    #delete not frequent relation
    for i in list(node_rel1):#get node dict
        for j in list(node_rel1[i]):#get rel dict
            if rel1_num[j]<x:#don't have enough source node
                node_rel1[i].pop(j)
    for i in list(node_rel2):#get node dict
        for j in list(node_rel2[i]):#get rel dict
            if rel2_num[j]<x-1:#don't have enough source node
                node_rel2[i].pop(j)
    print("delete: the number of relation with length 1:" + str(len(node_rel1)))
    print("delete: the number of relation with length 2:" + str(len(node_rel2)))

    for i in node_rel2:#get nodeid
        for j in node_rel2[i]:#get rel dict
            inter = (set(seed) & set(node_rel2[i][j])) - set([i])#get the number of elements of the intersection
            if len(inter)!=0:
                if j not in path:
                    path[j] = len(inter)
                else:
                    path[j] = path[j] + len(inter)
    print(f"number of path: {len(path)}")
    time2 = time.time()
    for k in node_rel1:
        for m in node_rel1[k]:
            for i in node_rel2:
                for j in node_rel2[i]:
                    if k!=i:#relation 1 vs relation 2 has different source node
                        inter = set(node_rel1[k][m]) & set(node_rel2[i][j]) - set(seed)#get target intersection
                        if len(inter)!=0:
                            print(inter)
                            rev = str(0-int(m))
                            if j+'_'+rev not in path:
                                path[j+'_'+rev] = 1
                            else:
                                path[j+'_'+rev] = path[j+'_'+rev] + 1

    time3 = time.time()
    print(f"time of finding length-3 path: {time3-time2}")
    print(f"number of path: {len(path)}")

    #add length-4 path
    for i in range(1, x+1):
        for j in range(1, x+1):
            if i!=j:
                for rm in node_rel2[int(seed[i-1])]:#get relid
                    for rk in node_rel2[int(seed[j-1])]:
                        inter = set(node_rel2[int(seed[i-1])][rm])-set(node_rel2[int(seed[j-1])][rk])-set(seed)
                        if len(inter)!=0:
                            #print(inter)
                            r = rk.strip().split('_')
                            opp1 = str(0-int(r[1]))
                            opp2 = str(0-int(r[0]))
                            p4 = rm + '_' + opp1 + '_' + opp2
                            #print(p4)
                            if p4 not in path:
                                path[p4] = 1
                            else:
                                path[p4] = path[p4]+1
    time4 = time.time()
    print(f"time of finding length-4 path: {time4-time3}")
    print(f"number of path: {len(path)}")

    end_time = time4-time0
    print(f"time of finding meta path: {time4-time0}")

    sum = 0#sum of seed pairs
    path_weight = {}#key is path, value is weight
    for p in path:
        if path[p]>=value:
            sum += path[p]
            path_weight[p] = path[p]
    for p in path_weight:
        path_weight[p] = path_weight[p]/sum
    print("the meta path with weight is: ")
    print(len(path_weight))
    return path_weight, len(path_weight), end_time




























