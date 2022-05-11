from model.get_matrix import pathmatrix
from tqdm import trange

def get_order(path_weight, seed, can, x, rel, rel_st, triple, start, end, pma):
    seed_set = set(seed)
    cand_set = set(can)
    canord = {}#key is candidate, value is order score
    merge = seed_set | cand_set

    for i in trange(len(can), desc="candidate"):#candidate
        cantmp = 0
        for j in range(x):#seed
            for k in path_weight:
                flag = 0#path contains candidate and seed or not
                seedtmp = 0
                if k not in pma:
                    matrix = pathmatrix(k, merge, seed_set, rel, rel_st, triple)
                    start[k] = matrix[0]#startlist
                    end[k] = matrix[1]#endlist
                    pma[k] = matrix[2]#matrix
                '''if (can[i] in start[k]) and (seed[j] in end[k]):
                    flag = pma[k][start[k].index(can[i]), end[k].index(seed[i])]#have relation'''
                if (can[i] in end[k]) and (seed[j] in start[k]):
                    flag = pma[k][start[k].index(seed[j]), end[k].index(can[i])]#have relation
                if flag != 0:
                    seedtmp = path_weight[k]+seedtmp
            cantmp += seedtmp
        cs = round(cantmp/float(x), 6)
        canord[can[i]] = cs

    orderlist = sorted(canord.items(), key=lambda x:x[1], reverse=True)
    return orderlist, pma, start, end








