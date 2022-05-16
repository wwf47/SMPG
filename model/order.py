from model.get_matrix import path_matrix
from tqdm import trange

def get_order(path_weight, seed, can, seed_num, rel, rel_st, triple, start, end, pma):
    seed_set = set(seed)
    can_set = set(can)
    can_ord = {}#key is candidate, value is order score
    merge = seed_set | can_set

    for i in trange(len(can), desc="candidate"):#candidate
        can_tmp = 0
        for j in range(seed_num):#seed
            seed_tmp = 0
            for k in path_weight:
                flag = 0#path contains candidate and seed or not
                if k not in pma:
                    matrix = path_matrix(k, merge, seed_set, rel, rel_st, triple)#based on path linking, relation seed can
                    start[k] = matrix[0]#startlist
                    end[k] = matrix[1]#endlist
                    pma[k] = matrix[2]#matrix
                if (can[i] in end[k]) and (seed[j] in start[k]):
                    flag = pma[k][start[k].index(seed[j]), end[k].index(can[i])]#have relation
                if flag != 0:
                    seed_tmp = path_weight[k]+seed_tmp

            can_tmp += seed_tmp
        cs = round(can_tmp/float(seed_num), 5)
        can_ord[can[i]] = cs

    order_list = sorted(can_ord.items(), key=lambda x:x[1], reverse=True)
    #print(order_list)
    return order_list, start, end








