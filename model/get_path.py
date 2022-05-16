from model.get_tree import Item, Tree
import time
from fractions import Fraction
import sys

def find_path(graph, seed, value, path_num, tree_deep, seed_num, tree_count):
    seed_pair = dict() # Key is seed_id, value is other seed
    ex_num = seed_num-1

    for i in range(seed_num):  # build l-1 dictionary
        seed_pair[seed[i]] = seed

    meta_tree = {}

    links = {} # rel key is seed_id, value is rel
    for s in seed:
        links[s] = set()
        node = graph.get(int(s))
        for t in node.link:
            tt = t.strip().split('_')
            links[s].add(tt[1])
            node1 = graph.get(int(tt[2]))
            for k in node1.link:
                rel2 = k.strip().split('_')
                links[s].add(rel2[1])

    rel_set = (links[seed[0]] & links[seed[1]]) | (links[seed[0]] & links[seed[2]]) | (links[seed[2]] & links[seed[1]]) # store relation
    meta_path = [] # each element is a string of the found meta path
    max_sim = dict()
    max_sim[0] = 0  # key 1 denotes the sim of max seed_num tree node
    max_sim[1] = []  # key 2 denotes the list consisting of key of max_num tree node
    mini_item = dict() # record the tree node with min item number
    mini_item[0] = -sys.maxsize -1# key 1 denotes the item number of  min item tree node
    mini_item[1] = ''  # key 2 denotes key(list consisting of the key) of  min item tree node
    max_sour = dict()
    max_sour[0] = 0  # key 1 denotes the num of max_num source node kind
    max_sour[1] = []

    tree = {} # key is rel_id, value is tree_node
    t1 = time.time()
    print('#####begin to find meta path#####')

    # initialize the root tree node
    root = Tree(0, 0)#edge is link
    for tem in seed:
        item = Item(tem, tem, 0)
        item.add_invited(tem)
        root.add_item(item)
        root.add_source(tem)
    tree['0'] = root
    first = 1  # the first expansion
    expand = 0

    while len(meta_path) < path_num and expand < tree_count:
        expand += 1
        if first == 1:
            for j in root.tree_item: # each seed
                sn = j.source # source
                source_node = graph[int(sn)] # get node
                for i in source_node.link: # each rel
                    tmp = i.strip().split('_')
                    if (tmp[1] in rel_set) or (tmp[1][1:] in rel_set) or (('-' + tmp[1]) in rel_set):#relation and reverse rel
                        if tmp[1] not in root.child: # relation neighbor
                            root.add_child(tmp[1])
                            if tmp[2] in seed_pair[tmp[0]]: # length-1 path
                                sim = 1
                            else:
                                sim = 0
                            it = Item(sn, tmp[2], sim) # information of relation
                            it.add_invited(sn)
                            it.add_invited(tmp[2])
                            tmp_tree = Tree(sim, 1)
                            tmp_tree.add_item(it)
                            tmp_tree.add_source(sn)
                            tree[tmp[1]] = tmp_tree
                        else:
                            if tmp[2] in seed_pair[tmp[0]]:
                                sim = 1
                            else:
                                sim = 0
                            it = Item(sn, tmp[2], sim)
                            it.add_invited(sn)
                            it.add_invited(tmp[2])
                            tree[tmp[1]].add_item(it)
                            tree[tmp[1]].tree_sim = tree[tmp[1]].tree_sim + sim # the similarity that represents whether node t is in the target node set of source node s
                            tree[tmp[1]].add_source(sn)
                    else:
                        pass

            first = 0
            t2 = time.time()
            print(f"time of the first expansion of tree completed: {str(t2 - t1)}")
            print(f"the num of tree_node after the first expansion: {str(len(tree))}")
            t = []

            for each in list(tree):
                if len(tree[each].child) == 0: # has no relation
                    if len(tree[each].source) < seed_num:
                        tree.pop(each) # need contain all seed node

            for e in tree:
                if tree[e].tree_sim > max_sim[0]:
                    max_sim[0] = tree[e].tree_sim
                    t = list()
                    t.append(e)
                elif tree[e].tree_sim == max_sim[0]:
                    t.append(e)
            max_sim[1] = t
            if max_sim[0] == 0:
                print("have no length-1 path")
            else:
                if max_sim[0] >= value:
                    for i in max_sim[1]:
                        meta_path.append(i)
                        meta_tree[i] = tree[i]
                print(f"the num of length-1 path is: {str(len(meta_path))}")
                for r in max_sim[1]:
                    tree.pop(r)#remove the length-1 relation

            max_sim[0] = 0
            max_sim[1] = []
            t3 = time.time()
            print(f"time of finding tree_node with max sim firstly: {str(t3 - t2)}")
        # find length-n path
        else:
            t = list()
            # get max source
            # choose the tree node with the max number of source set
            for j in tree:
                if (tree[j].tree_deep < tree_deep) and len(tree[j].child) == 0 and tree[j].tree_sim == 0:
                    if len(tree[j].source) > max_sour[0]:
                        max_sour[0] = len(tree[j].source)
                        t = list()
                        t.append(j)
                    elif len(tree[j].source) == max_sour[0]:
                        t.append(j)
            max_sour[1] = t
            #get minimum number of tuples
            if len(max_sour[1]) == 1:
                mini_item[0] = len(tree[max_sour[1][0]].tree_item)
                mini_item[1] = max_sour[1][0]
            elif len(max_sour[1]) > 1:
                for ec in max_sour[1]:
                    if len(tree[ec].tree_item) < int(mini_item[0]):
                        mini_item[0] = len(tree[ec].tree_item)
                        mini_item[1] = ec
            else:
                pass
            if mini_item[0] < 0:#end
                print(f"value of max tree_node[1]: {str(max_sim[1])}")
                break

            flag = 0
            # choose the minimum number of tuples to expand
            for j in tree[mini_item[1]].tree_item:
                sn = j.target
                node_i = graph[int(sn)]
                for k in node_i.link:
                    tmp = k.strip().split('_')
                    if (tmp[1] in rel_set) or (tmp[1][1:] in rel_set) or (('-' + tmp[1]) in rel_set):
                        if tmp[2] not in j.invited:
                            flag = 1#visit
                            vi = list()
                            vi.append(tmp[2])
                            if tmp[1] not in tree[mini_item[1]].child:
                                tree[mini_item[1]].add_child(tmp[1])#next rel
                                if tmp[2] in seed_pair[str(j.source)]:#find path
                                    sim = 1
                                else:
                                    sim = 0
                                it = Item(j.source, tmp[2], sim)
                                it.invited = j.invited + vi
                                tmp_tree = Tree(sim, tree[mini_item[1]].tree_deep + 1)
                                tmp_tree.add_item(it)
                                tmp_tree.add_source(j.source)
                                rel = mini_item[1] + '_' + tmp[1]
                                tree[rel] = tmp_tree
                            else:
                                if tmp[2] in seed_pair[str(j.source)]:
                                    sim = 1
                                else:
                                    sim = 0
                                it = Item(j.source, tmp[2], sim)
                                it.invited = j.invited + vi
                                rel = mini_item[1] + '_' + tmp[1]
                                tree[rel].add_item(it)
                                tree[rel].tree_sim = tree[rel].tree_sim + sim
                                tree[rel].add_source(j.source)
                    else:
                        pass
            max_value = sys.maxsize
            if flag == 0:
                tree[mini_item[1]].add_child(max_value)
                print(f"the num of tree_node until now: {str(len(tree))}")
            t = list()
            #get max sim
            for i in tree:
                if tree[i].tree_sim > max_sim[0]:
                    max_sim[0] = tree[i].tree_sim
                    t.clear()
                    t.append(i)
                elif tree[i].tree_sim == max_sim[1]:
                    t.append(i)
            max_sim[1] = t
            if max_sim[0] == 0:
                print("no path in this step")
            else:
                if max_sim[0] >= value:
                    for mm in max_sim[1]:
                        meta_path.append(mm)
                        meta_tree[mm] = tree[mm]
                        print(f"the item num within tree_node satisfying max sim: {str(len(tree[mm].tree_item))}")
                print(f"the num of meta path until now is: {str(len(meta_path))}")
                for j in max_sim[1]:
                    tree.pop(j)
            for k in list(tree):
                if (len(tree[k].child) == 0) and (tree[k].tree_sim == 0):
                    if len(tree[k].source) < ex_num:
                        tree.pop(k)
            max_sim[0] = 0
            max_sim[1] = []
            mini_item[0] = -sys.maxsize-1
            mini_item[1] = ''
            max_sour[0] = 0
            max_sour[1] = []

    end = time.time()
    sum_time = end - t1
    print(f"total time is : {sum_time}")
    print(f"find the meta path ending, the num is: {str(len(meta_path))}")
    print(f"the num of expansion: {str(tree_count)}")

    weight_sum = 0
    path_weight = {}
    path_seed_pairs = {}#get seed pair
    for i in meta_tree:
        mt = set()#seed pair
        print(i + ',similarity:' + str(meta_tree[i].tree_sim) + ',item_num:' + str(len(meta_tree[i].tree_item)))
        for j in meta_tree[i].tree_item:
            if j.sim == 1:#path link
                mt.add(j.source + ',' + j.target)
        path_weight[i] = Fraction(len(mt), seed_num * (seed_num - 1))
        print(f"the linking seed pair num of path, weight: {str(len(mt))} , {str(path_weight[i])}")

        weight_sum = weight_sum + path_weight[i]
        path_seed_pairs[i] = mt
    # normalized the weight
    for j in path_weight:
        path_weight[j] = Fraction(path_weight[j], weight_sum)
    return path_weight, len(path_weight), path_seed_pairs

