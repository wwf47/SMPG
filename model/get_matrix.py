from scipy.sparse import coo_matrix

def path_matrix(path, merge, seed, rel, rel_st, triple):#rel key is rel_id, value is source
    set2 = set()
    #triple = triple[:100]
    tmp = path.strip().split('_')
    list1 = list(set(rel[tmp[0]]) & seed)#source node
    #print(f"length of list1: {len(list1)}")
    for si in list1:
        set2 = set(rel_st[tmp[0]][si]) | set2#target
    list2 = list(set2 & set(rel[tmp[1]]))#second node
    #print(f"length of list2: {len(list2)}")

    if len(tmp) == 2:#path length is 2
        # print(f"path length is {len(tmp)}")
        list3 = list()
        for k2 in list2:
            list3 += rel_st[tmp[1]][k2]#third node
        list3 = list(set(list3) & merge)#belong to seed and candidate
        #print(f"length of list3: {len(list3)}")
        m1row = []
        m1col = []
        m1data = []
        for i in range(len(list1)):
            for j in range(len(list2)):
                if (list1[i]+'_'+tmp[0]+'_'+list2[j]) in triple:
                    m1row.append(i)
                    m1col.append(j)
                    m1data.append(1)

        m2row = []
        m2col = []
        m2data = []
        for i in range(len(list2)):
            for j in range(len(list3)):
                if (list2[i]+'_'+tmp[1]+'_'+list3[j]) in triple:
                    m2row.append(i)
                    m2col.append(j)
                    m2data.append(1)
        m1 = coo_matrix((m1data, (m1row, m1col)), shape=(len(list1), len(list2)))
        m2 = coo_matrix((m2data, (m2row, m2col)), shape=(len(list2), len(list3)))
        matrix = m1*m2
        return list1, list3, matrix

    if len(tmp) == 3:#path length is 3
        # print(f"path length is {len(tmp)}")
        list3 = []
        list4 = []
        for k2 in list2:
            list3.extend(rel_st[tmp[1]][k2])#get third node
        list3 = list(set(list3) & set(rel[tmp[2]]))
        for k3 in list3:
            list4.extend(rel_st[tmp[2]][k3])#get fourth node
        list4 = list(set(list4) & merge)#in candidate or seed

        m1row = []
        m1col = []
        m1data = []
        for i in range(len(list1)):
            for j in range(len(list2)):
                if (list1[i]+'_'+tmp[0]+'_'+list2[j]) in triple:
                    m1row.append(i)
                    m1col.append(j)
                    m1data.append(1)
        m2row = []
        m2col = []
        m2data = []
        for i in range(len(list2)):
            for j in range(len(list3)):
                if (list2[i]+'_'+tmp[1]+'_'+list3[j]) in triple:
                    m2row.append(i)
                    m2col.append(j)
                    m2data.append(1)
        m3row = []
        m3col = []
        m3data = []
        for i in range(len(list3)):
            for j in range(len(list4)):
                if (list3[i]+'_'+tmp[2]+''
                                        '_'+list4[j]) in triple:
                    m3row.append(i)
                    m3col.append(j)
                    m3data.append(1)
        m1 = coo_matrix((m1data, (m1row, m1col)), shape=(len(list1), len(list2)))
        m2 = coo_matrix((m2data, (m2row, m2col)), shape=(len(list2), len(list3)))
        m3 = coo_matrix((m3data, (m3row, m3col)), shape=(len(list3), len(list4)))
        mat = m1*m2
        matrix = mat*m3
        return list1, list4, matrix

    if len(tmp) == 4:#path length is 3
        # print(f"path length is {len(tmp)}")
        list3 = []
        list4 = []
        list5 = []
        for k2 in list2:
            list3.extend(rel_st[tmp[1]][k2])#get third node
        list3 = list(set(list3) & set(rel[tmp[2]]))
        for k3 in list3:
            list4.extend(rel_st[tmp[2]][k3])#get fourth node
        list4 = list(set(list4) & set(rel[tmp[3]]))
        for k4 in list4:
            list5.extend(rel_st[tmp[3]][k4])#get fifth node
        list5 = list(set(list5) & merge)

        m1row = []
        m1col = []
        m1data = []
        for i in range(len(list1)):
            for j in range(len(list2)):
                if (list1[i]+'_'+tmp[0]+'_'+list2[j]) in triple:
                    m1row.append(i)
                    m1col.append(j)
                    m1data.append(1)
        m2row = []
        m2col = []
        m2data = []
        for i in range(len(list2)):
            for j in range(len(list3)):
                if (list2[i]+'_'+tmp[1]+'_'+list3[j]) in triple:
                    m2row.append(i)
                    m2col.append(j)
                    m2data.append(1)
        m3row = []
        m3col = []
        m3data = []
        for i in range(len(list3)):
            for j in range(len(list4)):
                if (list3[i]+'_'+tmp[2]+'_'+list4[j]) in triple:
                    m3row.append(i)
                    m3col.append(j)
                    m3data.append(1)
        m4row = []
        m4col = []
        m4data = []
        for i in range(len(list4)):
            for j in range(len(list5)):
                if (list4[i]+'_'+tmp[3]+'_'+list5[j]) in triple:
                    m4row.append(i)
                    m4col.append(j)
                    m4data.append(1)
                    #m4[i][j] = 1
        m1 = coo_matrix((m1data, (m1row, m1col)), shape=(len(list1), len(list2)))
        m2 = coo_matrix((m2data, (m2row, m2col)), shape=(len(list2), len(list3)))
        m3 = coo_matrix((m3data, (m3row, m3col)), shape=(len(list3), len(list4)))
        m4 = coo_matrix((m4data, (m4row, m4col)), shape=(len(list4), len(list5)))
        mat = m1*m2
        mat1 = mat*m3
        matrix = mat1*m4

        return list1, list5, matrix










