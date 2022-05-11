from tqdm import tqdm

class Node:
    def __init__(self, nid):  # construction method,initialize
        self.nid = nid
        self.corrlink = []
    def setid(self, nid):
        self.nid = nid
    def appendcorrlink(self, link):
        self.corrlink.append(link)
    def getid(self):
        return self.nid
    def getcorrlink(self):
        return self.corrlink

def build_graph():
    node_set = {}

    with open("./data/yago/NodeNames.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Nodeset"):
            node = Node(2)
            tmp = line.strip().split('\t')
            node.setid(int(tmp[0]))
            node_set[int(tmp[0])] = node

    with open("./data/yago/onlyRecords.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Triple records"):
            tmp = line.strip().split('-')
            rel = node_set.get(int(tmp[0]))
            rel.appendcorrlink(tmp[0]+'_'+tmp[1]+'_'+tmp[2])
            revrel = node_set.get(int(tmp[2]))
            revrel.appendcorrlink(tmp[2]+'_'+'-'+tmp[1]+"_"+tmp[0])
    print("graph completed")
    return node_set

if __name__ == '__main__':
    node = build_graph()
    print(len(node))

