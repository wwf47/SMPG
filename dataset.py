
def get_seeds(data_dir, seeds):
    pos = []
    can = []
    data_pos = f"{data_dir}/{seeds}/positive.txt"
    data_can = f"{data_dir}/{seeds}/candidate.txt"
    with open(data_pos, "r") as f:
        for line in f.readlines():
            pos.append(line.strip())
    with open(data_can, "r") as f:
        for line in f.readlines():
            can.append(line.strip())

    print("the length of positive entity:" + str(len(pos)))
    print("the length of positive entity:" + str(len(can)))
    return pos, can

def get_links(data_dir):
    linkdict = {}#key is link and value is sourced node,all keys include link 8 and link -8
    linkst = {}# key is link and value is dict(key is source node of link ,value is target node of link)
    rec = []
    ref = f"{data_dir}/onlyRecords.txt"
    with open(ref, "r") as f:
        for line in f.readlines():
            tmp = line.strip().split("-")
            rec.append(tmp[0]+"_"+tmp[1]+"_"+tmp[2])
            rec.append(tmp[2] + "_" + "-"+tmp[1] + "_" + tmp[2])
            if tmp[1] not in linkdict.keys():
                linkdict[tmp[1]] = []
                linkdict[tmp[1]].append(tmp[2])
            if '-'+tmp[1] not in linkdict.keys():
                linkdict['-'+tmp[1]] = []
                linkdict['-' + tmp[1]].append(tmp[2])
            if tmp[1] not in linkst.keys():
                linkst[tmp[1]] = {}
            if tmp[0] not in linkdict[tmp[1]]:
                linkst[tmp[1]][tmp[0]] = []
                linkst[tmp[1]][tmp[0]].append(tmp[2])
            if '-'+tmp[1] not in linkst.keys():
                linkst['-'+tmp[1]] = {}
            if tmp[0] not in linkst['-'+tmp[1]]:
                linkst['-'+tmp[1]][tmp[0]] = []
                linkst['-'+tmp[1]][tmp[0]].append(tmp[2])
    print("the length of relation:" + str(len(linkdict)))
    print("the length of relation vs node:" + str(len(linkst)))
    print("the length of triple:" + str(len(rec)))
    return linkdict, linkst, rec




if __name__ == '__main__':
    data_dir = "data/seed"
    seeds = "demo"
    p, c = get_seeds(data_dir, seeds)
    a, b, d = get_links("data/yago")
