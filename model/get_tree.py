class items:
    def __init__(self, source, target, sim, invited):
        self.source = source
        self.target = target
        self.sim = sim
        self.invitednode = invited
    def setsource(self, source):
        self.source = source
    def settarget(self, target):
        self.target = target
    def setsim(self, sim):
        self.sim = sim
    def addinvited(self, n):
        self.invitednode.append(n)
    def getsource(self):
        return self.source
    def gettarget(self):
        return self.target
    def getsim(self):
        return self.sim
    def getinvited(self):
        return self.invitednode

class treenode:
    def __init__(self, tnodesim, treedeep):  # construction method,initialize
        self.tnodeitem = []
        self.tnodesim = tnodesim
        self.childnode = []
        self.treedeep = treedeep
        self.sour = set()
    def setdeep(self, deep):
        self.treedeep = deep
    def additem(self, node):
        self.tnodeitem.append(node)
    def setsim(self, sim):
        self.tnodesim = sim
    def getdeep(self):
        return self.treedeep
    def addchild(self, child):
        self.childnode.append(child)
    def getchild(self):
        return self.childnode
    def getitem(self):
        return self.tnodeitem
    def getsim(self):
        return self.tnodesim
    def addsourset(self, sor):
        self.sour.add(sor)
    def getsourset(self):
        return self.sour


if __name__=="__main__":
    n = items(1, 9, 0.8758, list())
    tree = treenode(1, 1.7, 2)