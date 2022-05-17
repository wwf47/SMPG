from model.get_graph import build_graph
import numpy as np
from argparse import ArgumentParser
from dataset import get_node, get_links, get_seeds
from model.get_path import find_path
from model.order import get_order
from eval_utils import eval_can


def init_args():
    parser = ArgumentParser()
    parser.add_argument("--seed", default="actor", type=str)
    parser.add_argument("--seed_num", default="3", type=int)
    parser.add_argument("--path_num", default="10", type=int)
    parser.add_argument("--tree_deep", default="4", type=int)
    parser.add_argument("--tree_count", default="200", type=int)

    arg = parser.parse_args()

    return arg


if __name__ == '__main__':
    args = init_args()
    # get positive and candidate
    pos, can = get_seeds("data/seed", args.seed)
    rel, rel_st, triple = get_links("data/yago")
    # Create a tree structure to store entity information and relationship information
    graph = build_graph("data/yago")
    node = get_node(graph)
    seed_num = args.seed_num  # seed number
    value = seed_num * (seed_num - 1) / 2 + 1  # predefined threshold value

    i, flag = 0, 3
    start = {}
    end = {}
    pma = {}
    p1 = []
    p2 = []
    p3 = []
    MAP = []
    end_set = set()

    for i in range(len(pos)-flag+1):
        seed = (pos[i:i+3])
        print("######Begin to get meta path and weight######")
        pw = find_path(graph, seed, value, args.path_num, args.tree_deep, seed_num, args.tree_count)
        print("######Begin to order the candidates######")
        order, s1, e1 = get_order(pw[0], seed, can, seed_num, rel, rel_st, triple, start, end, pma)
        res = eval_can(order, pos)
        p1.append(res[0])
        p2.append(res[1])
        p3.append(res[2])
        MAP.append(res[3])
        end_set = end_set | res[4]
        i += seed_num

    print(f"max, min, mean, variance of p@30: {str(max(p1))}, {str(min(p1))}, {str(np.mean(p1))}, {str(np.var(p1))}")
    print(f"max, min, mean, variance of p@60: {str(max(p2))}, {str(min(p2))}, {str(np.mean(p2))}, {str(np.var(p2))}")
    print(f"max, min, mean, variance of p@90: {str(max(p3))}, {str(min(p3))}, {str(np.mean(p3))}, {str(np.var(p3))}")
    print(f"max, min, mean, value of  MAP: {str(max(MAP)) + ',' + str(min(MAP)) + ',' + str(np.mean(MAP))}")















