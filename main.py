from model.get_graph import Node, build_graph
import numpy as np
import random
from tqdm import tqdm, trange
import os
from argparse import ArgumentParser
from dataset import get_node, get_links, get_seeds
from model.get_path import findpath

def init_args():
    parser = ArgumentParser()
    parser.add_argument("--seed", default="demo", type=str)
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
    rel, rel_st, triplet = get_links("data/yago")
    graph = build_graph()
    node = get_node(graph)
    x = 2
    simrang = x * (x - 1) / 2 + 1

    i, flag = 0, 2
    seedcom = []

    for i in trange(len(pos)-flag+1, desc="positive"):
        seed = []
        seed.append(pos[i])
        seed.append(pos[i+1])
        tmp = pos[i]+ '_'+ pos[i+1]
        seedcom.append(pos[i]+'_'+pos[i+1])
        print("######Begin to metapath and weight########")
        findpath(graph, seed, node, simrang, x)









