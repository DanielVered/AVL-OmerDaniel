import random
from avl_template_new import AVLNode, AVLTree

FUNCS_NAMES = ['insert', 'delete', 'search', 'join', 'split']

class FuncStats:
    def __init__(self, name: str):
        self.name = name
        self.n_trials = 0
        self.n_failures = 0
        self.failed_inputs = []


class AVLTester:
    def __init__(self, min_key: int, max_key: int, n_trees: int):
        assert 0 <= min_key <= max_key

        self.range = (min_key, max_key)
        self.n_trees = n_trees
        self.stats = {func: FuncStats(func) for func in FUNCS_NAMES}

    def update_failure(self, func_name: str, inputs: dict):
        self.stats[func_name].n_failures += 1
        self.stats[func_name].failed_inputs.append(inputs)

    def build_rand_tree(self, n_nodes: int) -> (AVLTree, int):
        tree = AVLTree()
        a, b = self.range

        self.stats['insert'].n_trials += n_nodes
        for _ in range(n_nodes):
            key = random.randint(a, b)
            try:
                tree.insert(key=key, val=None)
            except:
                self.update_failure(func_name='insert', inputs={'tree': tree, 'key': key})
        return tree

    def build_trees_arr(self) -> ([AVLTree], int):
        trees = []
        a, b = self.range

        for _ in range(self.n_trees):
            size = random.randint(max(a, 1), b)
            tree = self.build_rand_tree(n_nodes=size)
            trees.append(tree)

        return trees

    def get_rand_node(self, tree: AVLTree):
        size = tree.get_size()
        if size == 0:
            return None
        key = random.randint(0, size - 1)
        self.stats['search'].n_trials += 1
        try:
            node = tree.search(key)
            return node
        except:
            self.update_failure(func_name='search', inputs={'tree': tree, 'key': key})

    def delete_rand_nodes(self, trees: list[AVLTree]):
        for tree in trees:
            size = tree.get_size()
            if size in [0, 1]:
                nodes_to_delete = size
            else:
                nodes_to_delete = random.randint(1, size)
            self.stats['delete'].n_trials += nodes_to_delete
            for _ in range(nodes_to_delete):
                node = self.get_rand_node(tree)
                try:
                    tree.delete(node)
                except:
                    self.update_failure(func_name='delete', inputs={'tree': tree, 'node': node})

    def join_trees(self):
        pass

    def split_trees(self, trees: [AVLTree]):
        pass

    def is_bst_valid(self, node, min_val=float('-inf'), max_val=float('inf')) -> bool:
        if node is None:
            return True

        # Check if the current node key is within the valid range for BST
        if not (min_val < node.key < max_val):
            return False

        # Recursively check left and right subtrees with updated valid ranges
        return (self.is_bst_valid(node.left, min_val, node.key) and
                self.is_bst_valid(node.right, node.key, max_val))

    def is_avl_valid(self, tree: AVLTree) -> bool:
        root = tree.get_root()
        if root is None:
            return True

        # Check AVL properties
        return (self.is_avl_valid(root.get_left()) and
                self.is_avl_valid(root.get_right()) and
                abs(root.get_balance_factor()) <= 1)

    def is_valid_tree(self, tree: AVLTree) -> (bool, bool):
        is_bst = self.is_bst_valid(tree.get_root())
        is_avl = self.is_avl_valid(tree)
        return is_bst and is_avl

    def get_validity_after(self, trees: [AVLTree]):
        valid_rate = 1
        fraction = 1 / len(trees)
        for tree in trees:
            if not self.is_valid_tree(tree):
                valid_rate -= fraction
        return valid_rate


    def test(self):
        trees = self.build_trees_arr()
        print(f'validity rate after insert: {self.get_validity_after(trees)}')

        self.delete_rand_nodes(trees)
        print(f'validity rate after delete: {self.get_validity_after(trees)}')

    def print_stats(self):
        for func_name in self.stats.keys():
            print(f'----stats for: {func_name}')
            func_stats = self.stats[func_name]
            failure_rate = round(func_stats.n_failures / max(func_stats.n_trials, 1), 2)
            print(f'failure rate: {failure_rate}')

    def get_bad_inputs(self, func_name: str) -> [dict]:
        pass


tester = AVLTester(0, 100, 100)
tester.test()
tester.print_stats()

pass