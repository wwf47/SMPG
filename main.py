
from node import node

import numpy as np

import random
from argparse import ArgumentParser

def init_args():
    parser = ArgumentParser()
    parser.add_argument("--seed", default="demo", type=str)
    parser.add_argument("--max_seq_len", default=128, type=int)
    parser.add_argument("--model_path", default="./bert-base-uncased", type=str)
    parser.add_argument("--train_epoch", default=30, type=int)
    parser.add_argument("--do_train", default=True, type=bool)
    parser.add_argument("--do_eval", default=False, type=bool)
    parser.add_argument("--num_threads", default=1, type=int)
    parser.add_argument("--train_batch_size", default=16, type=int)
    parser.add_argument("--val_batch_size", default=16, type=int)
    parser.add_argument("--lr", default=3e-5, type=float, help="Learning rate for Adam")

    args = parser.parse_args()

    kg = f"./data/yago/onlyRecords.txt"
    args.kg = kg

    out_dir = f"./outputs"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    args.output_dir = out_dir

    return args



