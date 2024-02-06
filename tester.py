import random
from avl_template_new import AVLNode, AVLTree


class AVLTester:
    def __init__(self, min_key, max_key):
        self.range = (min_key, max_key)

    def build_rand_tree(self, n_nodes: int) -> AVLTree:
        tree = AVLTree()
        a, b = self.range
        for _ in range(n_nodes):
            try:
                tree.insert(key=random.randint(a, b), val=None)
            except:
                print('Problem with Insert!')
        return tree

    def build_trees_arr(self, n_trees: int):
        arr = []
        a, b = self.range
        for _ in range(n_trees):
            size = random.randint(a, b)
            arr.append(self.build_rand_tree(n_nodes=size))
        return arr

    def delete_rand_nodes(trees: list[AVLTree]):
        for tree in trees:
            nodes_to_delete = random.randint(1, tree.get_size() - 1)
            for _ in range(nodes_to_delete):
                key = random.randint(0, tree.get_size() - 1)
                tree.delete(tree.search(key))


    @staticmethod
    def is_valid_avl(tree: AVLTree) -> bool:
        pass

    def are_valid_avl_after(self, trees: [AVLTree], name: str, res: dict):
        n = len(trees)
        fraction = 1 / n

        res[name] = {'validity': 0, 'failure': 0}
        for tree in trees:
            try:
                if self.is_valid_avl(tree):
                    res[name]['validity'] += fraction
            except:
                res[name]['failure'] += fraction

    def test(self, n: int) -> {str: float}:
        res = {}

        trees = self.build_trees_arr(n)
        self.are_valid_avl_after(trees, name='insert', res=res)

        self.delete_rand_nodes()
        self.are_valid_avl_after(trees, name='delete', res=res)


tester = AVLTester(0, 100)
print(tester.test(10))
