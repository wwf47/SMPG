import unittest
from model.get_path import findpath
from dataset import get_node, get_links, get_seeds
from model.get_graph import build_graph
from model.order import get_order
seed = ['1', '5', '6']
x = 3
value = x * (x - 1) / 2 + 1
pathnum = 10
treedeep =4
treecount = 200
can = ['1', '2', '3', '4', '5', '6']
start = {}
end = {}
pma = {}
rel, rel_st, triple = get_links("./data/test")
graph = build_graph("./data/test")
node = get_node(graph)
pw = findpath(graph, seed, value, pathnum, treedeep, x, treecount)

class TestCase(unittest.TestCase):
    def test_path(self):
        self.assertEqual(2, pw[1])
    def test_order(self):
        order, s1, e1 = get_order(pw[0], seed, can, x, rel, rel_st, triple, start, end, pma)
        order_len = len(order)
        self.assertEqual(6, order_len)

def suite():
    tests = []
    # init the unit test suite
    suite = unittest.TestSuite()
    # add test cases
    case1 = TestCase("test_path")
    tests.append(case1)
    case2 = TestCase("test_order")
    tests.append(case2)

    suite.addTests(tests)

    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())

