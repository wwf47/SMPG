from model.get_tree import Item, Tree
import time
from fractions import Fraction
import sys


def visit(tree, tmp, relation, cur_item, seed_pair, item):
    if (tmp[1] in relation) or (tmp[1][1:] in relation) or (('-' + tmp[1]) in relation):
        vi = list()
        vi.append(tmp[2])
        if tmp[1] not in tree[cur_item].child:
            tree[cur_item].add_child(tmp[1])  # next rel
            if tmp[2] in seed_pair[str(item.source)]:  # find path
                sim = 1
            else:
                sim = 0
            it = Item(item.source, tmp[2], sim)
            if cur_item == '0':
                it.add_invited(item.source)
                it.add_invited(tmp[2])
                rel = tmp[1]
            else:
                it.invited = item.invited + vi
                rel = cur_item + '_' + tmp[1]
            tmp_tree = Tree(sim, tree[cur_item].tree_deep + 1)
            tmp_tree.add_item(it)
            tmp_tree.add_source(item.source)

            tree[rel] = tmp_tree
        else:
            if tmp[2] in seed_pair[str(item.source)]:
                sim = 1
            else:
                sim = 0
            it = Item(item.source, tmp[2], sim)
            if cur_item == '0':
                it.add_invited(item.source)
                it.add_invited(tmp[2])
                rel = tmp[1]
            else:
                it.invited = item.invited + vi
                rel = cur_item + '_' + tmp[1]
            tree[rel].add_item(it)
            tree[rel].tree_sim = tree[rel].tree_sim + sim
            tree[rel].add_source(item.source)


def path(cur_item, seed_pair, tree, graph, relation, meta_path, meta_tree, value, max_sim, ex_num):
    pre_time = time.time()
    flag = 0
    # choose the minimum number of tuples to expand
    if cur_item == '0':
        print("the first expand")
    else:
        print("continue expand")
    if cur_item != '':
        for item in tree[cur_item].tree_item:
            sn = item.target
            source_node = graph[int(sn)]
            for s in source_node.link:
                tmp = s.strip().split('_')
                if cur_item == 0:
                    visit(tree, tmp, relation, cur_item, seed_pair, item)
                else:
                    if tmp[2] not in item.invited:
                        visit(tree, tmp, relation, cur_item, seed_pair, item)
                    else:
                        pass

    max_value = sys.maxsize
    if flag == 0 and cur_item != '':
        tree[cur_item].add_child(max_value)
        print(f"the num of tree_node until now: {str(len(tree))}")
    t = list()
    # get max sim
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
    for e in list(tree):
        if (len(tree[e].child) == 0) and (tree[e].tree_sim == 0):
            if len(tree[e].source) < ex_num:
                tree.pop(e)

    cur_time = time.time()
    cost_time = cur_time-pre_time
    return cost_time


def find_path(graph, seed, value, path_num, tree_deep, seed_num, tree_count):
    seed_pair = dict()  # Key is seed_id, value is other seed
    ex_num = seed_num-1
    for i in range(seed_num):  # build l-1 dictionary
        seed_pair[seed[i]] = seed
    meta_tree = {}
    links = {}  # rel key is seed_id, value is rel
    meta_path = []  # each element is a string of the found meta path

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
    tree = {}  # key is rel_id, value is tree_node
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
    max_sim = dict()
    max_sim[0] = 0  # key 1 denotes the sim of max seed_num tree node
    max_sim[1] = []  # key 2 denotes the list consisting of key of max_num tree node
    mini_item = dict()  # record the tree node with min item number
    mini_item[0] = -sys.maxsize-1  # key 1 denotes the item number of  min item tree node
    mini_item[1] = ''  # key 2 denotes key(list consisting of the key) of  min item tree node
    max_sour = dict()
    max_sour[0] = 0  # key 1 denotes the num of max_num source node kind
    max_sour[1] = []

    while len(meta_path) < path_num and expand < tree_count:
        expand += 1
        cur_item = '0'
        if first == 0:
            tree_node = list()
            for t in tree:
                if (tree[t].tree_deep < tree_deep) and len(tree[t].child) == 0 and tree[t].tree_sim == 0:
                    if len(tree[t].source) > max_sour[0]:
                        max_sour[0] = len(tree[t].source)
                        tree_node.clear()
                        tree_node.append(t)
                    elif len(tree[t].source) == max_sour[0]:
                        tree_node.append(t)
            max_sour[1] = tree_node
            # get minimum number of tuples
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
            cur_item = mini_item[1]
        cost_time = path(cur_item, seed_pair, tree, graph, rel_set, meta_path, meta_tree, value, max_sim, ex_num)
        max_sim[0] = 0
        max_sim[1] = []
        mini_item[0] = -sys.maxsize-1
        mini_item[1] = ''
        max_sour[0] = 0
        max_sour[1] = []
        first = 0

        print(f"This step cost time: {cost_time}")
        '''if mini_item[0] < 0:
            break'''

    end = time.time()
    sum_time = end - t1
    print(f"total time is : {sum_time}")
    print(f"find the meta path ending, the num is: {str(len(meta_path))}")
    print(f"the num of expansion: {str(tree_count)}")

    weight_sum = 0
    path_weight = {}
    path_seed_pairs = {}  # get seed pair
    for i in meta_tree:
        mt = set()  # seed pair
        print(i + ',similarity:' + str(meta_tree[i].tree_sim) + ',item_num:' + str(len(meta_tree[i].tree_item)))
        for j in meta_tree[i].tree_item:
            if j.sim == 1:  # path link
                mt.add(j.source + ',' + j.target)
        path_weight[i] = Fraction(len(mt), seed_num * (seed_num - 1))
        print(f"the linking seed pair num of path, weight: {str(len(mt))} , {str(path_weight[i])}")
        weight_sum = weight_sum + path_weight[i]
        path_seed_pairs[i] = mt
    # normalized the weight
    for j in path_weight:
        path_weight[j] = Fraction(path_weight[j], weight_sum)
    return path_weight, len(path_weight), path_seed_pairs

