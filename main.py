from model.get_graph import Node, build_graph
import numpy as np
import random
from tqdm import tqdm, trange
import os
from argparse import ArgumentParser
from dataset import get_node, get_links, get_seeds
from model.get_path import findpath
from model.order import get_order
from eval_utils import eval

def init_args():
    parser = ArgumentParser()
    parser.add_argument("--seed", default="actor", type=str)
    args = parser.parse_args()

    kg = f"./data/yago/onlyRecords.txt"
    args.kg = kg

    out_dir = f"./outputs"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    args.output_dir = out_dir

    return args


if __name__=='__main__':
    args = init_args()
    pos, can = get_seeds("data/seed", args.seed)
    rel, rel_st, triple = get_links("data/yago")
    graph = build_graph()
    node = get_node(graph)
    x = 2
    simrang = x * (x - 1) / 2 + 1

    i, flag = 0, 2
    seedcom = []
    seedpath = {}
    seedtime = {}
    sum_time = 0
    start = {}
    end = {}
    pma = {}
    p1 = []
    p2 = []
    p3 = []
    MAP = []
    endset = set()

    for i in trange(len(pos)-flag+1, desc="positive"):
        seed = []
        seed.append(pos[i])
        seed.append(pos[i+1])
        tmp = pos[i]+'-'+pos[i+1]
        seedcom.append(pos[i]+'-'+pos[i+1])
        print("######Begin to get metapath and weight######")
        pw = findpath(seed, node, simrang, x)
        seedpath[tmp] = pw[0]
        seedtime[tmp] = pw[2]
        sum_time += pw[2]
        print("######Begin to order the candidates######")
        order, pma, s1, e1 = get_order(pw[0], seed, can, x, rel, rel_st, triple, start, end, pma)
        res = eval(order, pos)
        p1.append(res[0])
        p2.append(res[1])
        p3.append(res[2])
        MAP.append(res[3])
        endset = endset|res[4]

        i += x
    prenum = len(endset & set(pos))

    print(f"max, min, mean, variance of p@30: {str(max(p1))}, {str(min(p1))}, {str(np.mean(p1))}, {str(np.var(p1))}")
    print(f"max, min, mean, variance of p@60: {str(max(p2))}, {str(min(p2))}, {str(np.mean(p2))}, {str(np.var(p2))}")
    print(f"max, min, mean, variance of p@90: {str(max(p3))}, {str(min(p3))}, {str(np.mean(p3))}, {str(np.var(p3))}")
    print(f"correct num: {str(prenum)}")
    print(f"precision: {str(float(prenum)/len(endset))}")
    print(f"recall: {str(float(prenum)/len(pos))}")
















