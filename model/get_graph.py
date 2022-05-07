from tqdm import tqdm

class Node:
    def __init__(self, nid, name):  # construction method,initialize
        self.nid = nid
        self.name = name
        self.corrlink = []
        self.nodetype = []
    def setid(self, nid):
        self.nid = nid
    def setname(self, name):
        self.name = name
    def appendtype(self, ty):
        self.nodetype.append(ty)
    def appendcorrlink(self, link):
        self.corrlink.append(link)
    def getid(self):
        return self.nid
    def getname(self):
        return self.name
    def gettype(self):
        return self.nodetype
    def getcorrlink(self):
        return self.corrlink
    def judgetype(self, ty):
        temp = False
        if ty in self.nodetype:
            temp = True
        return temp

def build_graph():
    type_set = {}
    node_set = {}

    with open("./data/yago/Type-NodeTable.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Typeset"):
            if line == '\n':
                continue
            tmp = line.strip().split('-')
            type_set[int(tmp[1])] = tmp[0].strip()

    with open("./data/yago/NodeNames.txt", "r") as f:
        #cont = 0
        for line in tqdm(f.readlines(), desc="Nodeset"):
            node = Node(2, 'wwf')
            #cont += 1
            #if cont%200000==0:
                #print(cont)
            tmp = line.strip().split('\t')
            node.setid(int(tmp[0]))
            node.setname(tmp[1])
            tp = type_set.get(int(tmp[0]))#get the type of node
            for t in tp.split(' '):
                node.appendtype(int(t))
            node_set[int(tmp[0])] = node

    #cont = 0
    with open("./data/yago/onlyRecords.txt", "r") as f:
        for line in tqdm(f.readlines(), desc="Triple records"):
            #cont += 1
            #if cont%500000 == 0:
                #print(cont)
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

