import unittest
from model.get_path import findpath
from dataset import get_node, get_links, get_seeds
from model.get_graph import build_graph
seed = ['1', '5']
x = 2
value = x * (x - 1) / 2 + 1
rel, rel_st, triple = get_links("data/test")
graph = build_graph("data/test")
node = get_node(graph)


class TestCase(unittest.TestCase):
    def test_demo(self):
        path, path_len, _ = findpath(seed, node, value, x)
        self.assertEqual(2, path_len)


def suite():
    tests = []
    suite = unittest.TestSuite()

    case1 = TestCase("test_demo")
    tests.append(case1)

    suite.addTests(tests)

    return suite

if __name__ == "__main__":


    runner = unittest.TextTestRunner()
    runner.run(suite())

