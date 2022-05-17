from scipy.sparse import coo_matrix


def cur_path(rel, start, end, triple):
    row = []
    col = []
    data = []
    for i in range(len(start)):
        for j in range(len(end)):
            if (start[i] + '_' + rel + '_' + end[j]) in triple:
                row.append(i)
                col.append(j)
                data.append(1)
    matrix = coo_matrix((data, (row, col)), shape=(len(start), len(end)))
    return matrix


def path_matrix(path, merge, seed, rel, rel_st, triple):  # rel key is rel_id, value is source
    set2 = set()
    # triple = triple[:100]
    tmp = path.strip().split('_')
    list1 = list(set(rel[tmp[0]]) & seed)  # source node
    # print(f"length of list1: {len(list1)}")
    for si in list1:
        set2 = set(rel_st[tmp[0]][si]) | set2  # target
    list2 = list(set2 & set(rel[tmp[1]]))  # second node
    # print(f"length of list2: {len(list2)}")

    pre_list = list2
    pre_matrix = cur_path(tmp[0], list1, list2, triple)
    end_list = list2

    for i in range(1, len(tmp)-1):
        print(i)
        print(f"relation: {tmp[i]}")
        cur_list = list()
        for p in pre_list:
            cur_list.extend(rel_st[tmp[i]][p])
        if i < len(tmp)-1:
            cur_list = list(set(cur_list) & set(rel[tmp[i+1]]))
        else:
            cur_list = list(set(cur_list) & merge)
        cur_matrix = cur_path(tmp[i], pre_list, cur_list, triple)
        pre_matrix = pre_matrix*cur_matrix
        end_list = cur_list
        pre_list = cur_list

    return list1, end_list, pre_matrix








