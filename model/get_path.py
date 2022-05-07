import time
import random
import collections
from fractions import Fraction

def findpath(graph, seed, node, simrang, x):
    node_rel1 = {}#key is nid, value is rel dict
    node_rel2 = {}#key is nid, value is relation path
    rel1 = []
    rel2 = []
    link = {}
    path = {}#key is path, value is number of (source,target)
    path_weight = {}
    start_time = time.time()
    for i in seed:
        link[int(i)] = {}
        node_rel1[int(i)] = node[int(i)]
        print("the link related to node is: "+str(len(node[int(i)].keys())))
        for j in node[int(i)].keys():#get relid(dictk)
            rel1.append(j)
            for k in node[int(i)][j]:#get target nid(list)
                for m in node[int(k)].keys():#get relid
                    #add relation path
                    if j+'_'+m not in link[int(i)].keys():
                        rel2.append(j+'_'+m)
                        link[int(i)][j+'_'+m] = []
                    link[int(i)][j+'_'+m] = link[int(i)][j+'_'+m]+node[int(k)][m]#get next relation related nodes
        node_rel2[int(i)] = link[int(i)]
        print('the dictionary of relation with length 2 has been built,the number is:')
    for s in seed:
        print(len(link[int(s)].keys()))

    #record the seed count of each 1-relation contains
    d1 = collections.Counter(rel1)
    rel1_num = dict(d1)
    d2 = collections.Counter(rel2)
    rel2_num = dict(d2)

    print("origin: the number of relation with length 1:"+str(len(node_rel1)))
    print("origin: the number of relation with length 2:"+str(len(node_rel2)))

    #maximum number of source set
    #delete not frequent relation
    for i in list(node_rel1.keys()):#get node dict
        for j in list(node_rel1[i].keys()):#get rel dict
            if rel1_num[j]<x:#don't have enough source node
                node_rel1[i].pop(j)
    for i in list(node_rel2.keys()):#get node dict
        for j in list(node_rel2[i].keys()):#get rel dict
            if rel2_num[j]<x-1:#don't have enough source node
                node_rel2[i].pop(j)
    print("delete: the number of relation with length 1:" + str(len(node_rel1)))
    print("delete: the number of relation with length 2:" + str(len(node_rel2)))

    for i in node_rel2.keys():#get nodeid
        for j in node_rel2[i].keys():#get rel dict
            inter = (set(seed) & set(node_rel2[i][j])) - set([i])#get the number of elements of the intersection
            if len(inter)!=0:
                if j not in path.keys():
                    path[j] = len(inter)
                else:
                    path[j] = path[j] + len(inter)
    time0 = time.time()
    for k in node_rel1.keys():
        for m in node_rel1[k].keys():
            for i in node_rel2.keys():
                for j in node_rel2[i].keys():
                    if k!=i:#relation 1 vs relation 2 has different source node
                        inter = set(node_rel1[k][m]) & set(node_rel2[i][j]) - set(seed)#get target intersection
                        if len(inter)!=0:
                            print(inter)
                            rev = str(0-int(m))
                            if j+'_'+rev not in path.keys():
                                path[j+'_'+rev] = 1
                            else:
                                path[j+'_'+rev] = path[j+'_'+rev] + 1

    time1 = time.time()
    print(f"time of finding length-3 path: {time1-time0}")

    for i in range(1, x+1):
        for j in range(1, x+1):
            if i!=j:
                for rm in node_rel2[int(seed[i-1])].keys():#get relid
                    for rk in node_rel2[int(seed[j-1])].keys():
                        inter = set(node_rel2[int(seed[i-1])][rm])-set(node_rel2[int(seed[j-1])][rk])-set(seed)
                        if len(inter)!=0:
                            print(inter)
                            




















