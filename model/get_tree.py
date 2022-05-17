class Item:
    def __init__(self, source, target, sim):
        self.source = source
        self.target = target
        self.sim = sim
        self.invited = []

    def add_invited(self, node):
        self.invited.append(node)


class Tree:
    def __init__(self, tree_sim, tree_deep):
        self.tree_item = []
        self.tree_sim = tree_sim
        self.child = []
        self.tree_deep = tree_deep
        self.source = set()

    def add_item(self, node):
        self.tree_item.append(node)

    def add_child(self, node):
        self.child.append(node)

    def add_source(self, sor):
        self.source.add(sor)


if __name__ == "__main__":
    n = Item(1, 9, 0.8758)
    tree = Tree(1, 1.7)
    tree.child.append(2)

