from model.get_tree import items
from model.get_tree import treenode
import time
from fractions import Fraction
import sys

def findpath(graph, seed, value, pathnum, treedeep, x, treecount):
    seedpair = {}#key is seedid, value is other seed
    expan_num = x-1

    for i in range(x):  # build l-1 dictionary
        seedpair[seed[i]] = seed

    metatree = {}

    link = {}#rel key is seedid, value is rel
    for i in seed:
        link[i] = set()
        node = graph.get(int(i))
        for j in node.getcorrlink():
            rel1 = j.strip().split('_')
            link[i].add(rel1[1])
            node1 = graph.get(int(rel1[2]))
            for k in node1.getcorrlink():
                rel2 = k.strip().split('_')
                link[i].add(rel2[1])

    node_rel = (link[seed[0]] & link[seed[1]]) | (link[seed[0]] & link[seed[2]]) | (link[seed[2]] & link[seed[1]])#store relation
    metapath = [] # each element is a string of the found meta path
    #keylist = seedpair.keys()#seedlist
    maxsim = {}
    maxsim[1] = 0  # key 1 denotes the sim of max tree node
    maxsim[2] = []  # key 2 denotes the list consisting of key of max tree node
    minitem = {} # record the tree node withmin item number
    minitem[1] = -sys.maxsize -1# key 1 denotes the item number of  min item tree node
    minitem[2] = ''  # key 2 denotes key(list consisting of the key) of  min item tree node
    maxsour = {}
    maxsour[1] = 0  # key 1 denotes the num of max source node kind
    maxsour[2] = []

    tree = {}#key is relid, value is treenode
    t1 = time.time()
    print('#####begin to find meta path#####')

    # inialize the root tree node
    root = treenode(3.98, 0)#edge is link
    for tem in seed:
        item = items(tem, tem, 0, list())
        item.addinvited(tem)
        root.additem(item)
        root.addsourset(tem)
    root.setsim(0)

    tree['0'] = root
    first = 1  #the first expansion
    expand = 0

    while len(metapath) < pathnum and expand < treecount:
        expand += 1
        if first == 1:
            for j in root.getitem():#each seed
                sn = j.getsource()#source
                source_node = graph[int(sn)]#get node
                for i in source_node.getcorrlink():#each rel
                    tmp = i.strip().split('_')
                    if (tmp[1] in node_rel) or (tmp[1][1:] in node_rel) or (('-' + tmp[1]) in node_rel):#relation and reverse rel
                        if tmp[1] not in root.getchild():#relation neighbor
                            root.addchild(tmp[1])
                            tmptree = treenode(3.98, 1)#init chid, deep is 1
                            if tmp[2] in seedpair[tmp[0]]:#length-1 path
                                sim = 1
                            else:
                                sim = 0
                            it = items(sn, tmp[2], sim, list())#information of relation
                            it.addinvited(sn)
                            it.addinvited(tmp[2])
                            tmptree.additem(it)
                            tmptree.setsim(sim)
                            tmptree.addsourset(sn)
                            tree[tmp[1]] = tmptree
                        else:
                            if tmp[2] in seedpair[tmp[0]]:
                                sim = 1
                            else:
                                sim = 0
                            it = items(sn, tmp[2], sim, list())
                            it.addinvited(sn)
                            it.addinvited(tmp[2])
                            tree[tmp[1]].additem(it)
                            tree[tmp[1]].setsim(tree[tmp[1]].getsim() + sim)#the similarity that represents whether node t is in the target node set of source node s
                            tree[tmp[1]].addsourset(sn)
                    else:
                        pass

            first = 0
            t2 = time.time()
            print(f"time of the first expansion of tree completed: {str(t2 - t1)}")
            print(f"the num of treenode after the first expansion: {str(len(tree))}")
            t = []

            for each in list(tree):
                if len(tree[each].getchild()) == 0:#has no relation
                    if len(tree[each].getsourset()) < x:
                        tree.pop(each)#need contain all seed node

            for e in tree:
                if tree[e].getsim() > maxsim[1]:
                    maxsim[1] = tree[e].getsim()
                    t = []
                    t.append(e)
                elif tree[e].getsim() == maxsim[1]:
                    t.append(e)
            maxsim[2] = t
            if maxsim[1] == 0:
                print("have no length-1 path")
            else:
                if maxsim[1] >= value:
                    for i in maxsim[2]:
                        metapath.append(i)
                        metatree[i] = tree[i]
                print(f"the num of length-1 path is: {str(len(metapath))}")
                for r in maxsim[2]:
                    tree.pop(r)#remove the length-1 relation

            maxsim[1] = 0
            maxsim[2] = []
            t3 = time.time()
            print(f"time of finding treenode with max sim firstly: {str(t3 - t2)}")
        # find length-n path
        else:
            t = []
            # get max source
            # choose the tree node with the maximum number of source set
            for j in tree:
                if ((tree[j].getdeep() < treedeep) and len(tree[j].getchild()) == 0 and tree[j].getsim() == 0):
                    if len(tree[j].getsourset()) > maxsour[1]:
                        maxsour[1] = len(tree[j].getsourset())
                        t = []
                        t.append(j)
                    elif len(tree[j].getsourset()) == maxsour[1]:
                        t.append(j)
            maxsour[2] = t
            #get minimum number of tuples
            if len(maxsour[2]) == 1:
                minitem[1] = len(tree[maxsour[2][0]].getitem())
                minitem[2] = maxsour[2][0]
            elif len(maxsour[2]) > 1:
                for ec in maxsour[2]:
                    if len(tree[ec].getitem()) < int(minitem[1]):
                        minitem[1] = len(tree[ec].getitem())
                        minitem[2] = ec
            else:
                pass
            if minitem[1] < 0:#end
                print(f"value of maxsimtreenode[1]: {str(maxsim[1])}")
                break

            flag = 0
            # choose the minimum number of tuples to expand
            for j in tree[minitem[2]].getitem():
                sn = j.gettarget()
                nodei = graph[int(sn)]
                for k in nodei.getcorrlink():
                    tmp = k.strip().split('_')
                    if (tmp[1] in node_rel) or (tmp[1][1:] in node_rel) or (('-' + tmp[1]) in node_rel):
                        if tmp[2] not in j.getinvited():
                            flag = 1#visit
                            vi = []
                            vi.append(tmp[2])
                            if tmp[1] not in tree[minitem[2]].getchild():
                                tree[minitem[2]].addchild(tmp[1])#next rel
                                tmptree = treenode(3.98, tree[minitem[2]].getdeep() + 1)
                                if tmp[2] in seedpair[str(j.getsource())]:#find path
                                    sim = 1
                                else:
                                    sim = 0
                                it = items(j.getsource(), tmp[2], sim, j.getinvited() + vi)
                                tmptree.additem(it)
                                tmptree.setsim(sim)
                                tmptree.addsourset(j.getsource())
                                rel = minitem[2] + '_' + tmp[1]
                                tree[rel] = tmptree
                            else:
                                if tmp[2] in seedpair[str(j.getsource())]:
                                    sim = 1
                                else:
                                    sim = 0
                                it = items(j.getsource(), tmp[2], sim, j.getinvited() + vi)
                                rel = minitem[2] + '_' + tmp[1]
                                tree[rel].additem(it)
                                tree[rel].setsim(tree[rel].getsim() + sim)
                                tree[rel].addsourset(j.getsource())
                    else:
                        pass
            if flag == 0:
                tree[minitem[2]].addchild('88888888')
                print(f"the num of treenode untill now: {str(len(tree))}")
            t = []
            #get max sim
            for i in tree:
                if tree[i].getsim() > maxsim[1]:
                    maxsim[1] = tree[i].getsim()
                    t = []
                    t.append(i)
                elif tree[i].getsim() == maxsim[1]:
                    t.append(i)
            maxsim[2] = t
            if maxsim[1] == 0:
                print("no path in this step")
            else:
                if maxsim[1] >= value:
                    for mm in maxsim[2]:
                        metapath.append(mm)
                        metatree[mm] = tree[mm]
                        print(f"the item num within treenode satisfying max sim: {str(len(tree[mm].getitem()))}")
                print(f"the num of meta path until now is: {str(len(metapath))}")
                for j in maxsim[2]:
                    tree.pop(j)
            for k in list(tree):
                if (len(tree[k].getchild()) == 0) and (tree[k].getsim() == 0):
                    if len(tree[k].getsourset()) < expan_num:
                        tree.pop(k)
            maxsim[1] = 0
            maxsim[2] = []
            minitem[1] = -sys.maxsize-1
            minitem[2] = ''
            maxsour[1] = 0
            maxsour[2] = []

    end = time.time()
    alltime = end - t1
    print(f"total time is : {alltime}")
    print(f"find the meta path ending, the num is: {str(len(metapath))}")
    print(f"the num of expansion: {str(treecount)}")

    weight_sum = 0
    pathweight = {}
    pathseedpairs = {}#get seed pair
    for i in metatree:
        mt = set()#seed pair
        print(i + ',sim:' + str(metatree[i].getsim()) + ',itemnum:' + str(len(metatree[i].getitem())))
        for j in metatree[i].getitem():
            if j.getsim() == 1:#path link
                mt.add(j.getsource() + ',' + j.gettarget())
        pathweight[i] = Fraction(len(mt), x * (x - 1))
        print("the linking seed pair num of path, weight:" + str(len(mt)) + ',' + str(pathweight[i]))

        weight_sum = weight_sum + pathweight[i]
        pathseedpairs[i] = mt
    # normalized the weight
    for j in pathweight:
        pathweight[j] = Fraction(pathweight[j], weight_sum)
    return pathweight, len(pathweight), pathseedpairs

