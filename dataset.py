from model.get_graph import build_graph

def get_seeds(data_path, seed):
    pos = []
    can = []
    data_pos = f"{data_path}/{seed}/positive.txt"
    data_can = f"{data_path}/{seed}/candidate.txt"
    with open(data_pos, "r") as f:
        for line in f.readlines():
            pos.append(line.strip())
    with open(data_can, "r") as f:
        for line in f.readlines():
            can.append(line.strip())

    print(f"the length of positive entity: {str(len(pos))}")
    print(f"the length of candidate entity: {str(len(can))}")
    return pos, can

def get_links(data_path):
    link_dict = {}#key is link and value is sourced node,all keys include link 8 and link -8
    link_st = {}# key is link and value is dict(key is source node of link ,value is target node of link)
    ref = f"{data_path}/records.txt"
    rec = []
    with open(ref, "r") as f:
        for line in f.readlines():
            tmp = line.strip().split("-")
            rec.append(tmp[0]+"_"+tmp[1]+"_"+tmp[2])
            rec.append(tmp[2]+"_"+"-"+tmp[1]+"_"+tmp[0])
            if tmp[1] not in link_dict:
                link_dict[tmp[1]] = []
            link_dict[tmp[1]].append(tmp[0])
            if '-'+tmp[1] not in link_dict:
                link_dict['-'+tmp[1]] = []
            link_dict['-'+tmp[1]].append(tmp[2])
            if tmp[1] not in link_st:
                link_st[tmp[1]] = {}
            if tmp[0] not in link_st[tmp[1]]:
                link_st[tmp[1]][tmp[0]] = []
            link_st[tmp[1]][tmp[0]].append(tmp[2])
            if '-'+tmp[1] not in link_st:
                link_st['-'+tmp[1]] = {}
            if tmp[2] not in link_st['-'+tmp[1]]:
                link_st['-'+tmp[1]][tmp[2]] = []
            link_st['-'+tmp[1]][tmp[2]].append(tmp[0])
    print("the length of relation:" + str(len(link_dict)))
    print("the length of relation vs node:" + str(len(link_st)))
    print("the length of triple:" + str(len(rec)))
    return link_dict, link_st, rec

def get_node(graph):
    node_link = {}  # key is node and value is dict(key is link connecting node and value is node )
    for i in graph:
        rel = {}#key is rel_id and value is list of target node
        for j in graph[i].link:
            arr = j.strip().split('_')
            if arr[1] not in rel:
                rel[arr[1]] = []
            rel[arr[1]].append(arr[2])
        node_link[i] = rel
    #print("the length of node:" + str(len(node_link)))
    return node_link

if __name__ == '__main__':
    data_dir = "data/test"
    seeds = "actor"
    #p, c = get_seeds(data_dir, seeds)
    a, b, d = get_links(data_dir)
    graph = build_graph(data_dir)
    node = get_node(graph)
