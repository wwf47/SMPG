class Node:
    def __init__(self, nid, name):  # construction method,initialize
        self.nid = nid
        self.name = name
        self.corrlink = []
        self.nodetype = []
    def setno(self, nid):
        self.nid = nid
    def setname(self, name):
        self.name = name
    def appendtype(self, ty):
        self.nodetype.append(ty)
    def appendcorrlink(self, link):
        self.corrlink.append(link)
    def getno(self):
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

    print("begin to load typeset")

    with open("./data/yago/Type-NodeTable.txt", "r") as f:
        for line in f.readlines():
            if line == '\n':
                continue
            tmp = line.strip().split('-')
            type_set[int(tmp[1])] = tmp[0].strip()
    print("load typeset finished")

    with open("./data/yago/NodeNames.txt", "r") as f:
        cont = 0
        for line in f.readlines():
            node = Node(2, 'wwf')
            cont += 1
            if cont%200000==0:
                print(cont)
            if line == '\n':
                continue
            tmp = line.strip().split('-')
            type_set[int(tmp[1])] = tmp[0].strip()
    print("load typeset finished")
