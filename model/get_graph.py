from tqdm import tqdm

class Node:
    def __init__(self, nid):
        self.nid = nid
        self.link = []
    def add_link(self, link):
        self.link.append(link)

def build_graph(data_dir):
    node_dic = {}#key is node_id, value is Tree_node

    with open(f"{data_dir}/NodeNames.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Nodeset"):
            tmp = line.strip().split('\t')
            nodes = Node(int(tmp[0]))
            node_dic[int(tmp[0])] = nodes

    with open(f"{data_dir}/records.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Triple records"):
            tmp = line.strip().split('-')
            rel = node_dic[int(tmp[0])]
            rel.add_link(tmp[0]+'_'+tmp[1]+'_'+tmp[2])
            rev_rel = node_dic[int(tmp[2])]
            rev_rel.add_link(tmp[2]+'_'+'-'+tmp[1]+"_"+tmp[0])
    print("graph completed")
    return node_dic

if __name__ == '__main__':
    node = build_graph(data_dir="../data/test")
    for i in node:
        print(node[i].add_link(1))
        print(node[i].nid)

