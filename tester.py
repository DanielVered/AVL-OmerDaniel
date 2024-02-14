import random
from avl_template_new import AVLNode, AVLTree

FUNCS_NAMES = ['insert', 'delete', 'search', 'split', 'join']


class FuncStats:
    def __init__(self, name: str):
        self.name = name
        self.n_trials = 0
        self.n_failures = 0
        self.failed_inputs = []
        self.n_invalid_trees = 0  # not an AVL/BST
        self.invalid_trees = []  # not an AVL/BST
        self.n_invalid_size = 0
        self.invalid_size_trees = []
        self.n_invalid_edge = 0  # min/max are invalid
        self.invalid_edge_trees = []  # min/max are invalid


class AVLTester:
    def __init__(self, min_key: int, max_key: int, n_trees: int):
        assert 0 <= min_key <= max_key

        self.range = (min_key, max_key)
        self.n_trees = n_trees
        self.stats = {func: FuncStats(func) for func in FUNCS_NAMES}

    def update_failure(self, func_name: str, inputs: dict):
        self.stats[func_name].n_failures += 1
        self.stats[func_name].failed_inputs.append(inputs)

# -------------------------------- Action Performers -------------------------------- #
    def build_rand_tree(self, n_nodes: int) -> AVLTree:
        tree = AVLTree()
        a, b = self.range

        self.stats['insert'].n_trials += n_nodes
        keys = [n + 1 for n in range(n_nodes)]
        random.shuffle(keys)

        for key in keys:
            try:
                tree.insert(key=key, val=key)
            except BaseException as err:
                msg = str(err)
                self.update_failure(func_name='insert', inputs={'tree': tree, 'key': key, 'exception': msg})
        return tree

    def build_trees_arr(self) -> ([AVLTree], int):
        trees = []
        a, b = self.range

        for _ in range(self.n_trees):
            size = random.randint(max(a, 0), b)
            trees.append(self.build_rand_tree(n_nodes=size))

        return trees

    def get_rand_node(self, tree: AVLTree):
        if tree.size == 0:
            return None
        key = random.choice(tree.avl_to_array())[0]
        self.stats['search'].n_trials += 1
        try:
            node = tree.node_search(key)
            return node
        except:
            self.update_failure(func_name='search', inputs={'tree': tree, 'key': key})

    def delete_rand_nodes(self, trees: list[AVLTree]):
        for tree in trees:
            size = tree.size
            if size in [0, 1]:
                nodes_to_delete = size
            else:
                nodes_to_delete = random.randint(1, size)
            self.stats['delete'].n_trials += nodes_to_delete
            for _ in range(nodes_to_delete):
                node = self.get_rand_node(tree)
                try:
                    tree.delete(node)
                except BaseException as err:
                    msg = str(err)
                    self.update_failure(func_name='delete', inputs={'tree': tree, 'node': node, 'exception': msg})

    def split_trees(self, trees: [AVLTree]) -> [AVLTree]:
        split_trees = {'trees': [], 'nodes': []}
        for tree in trees:
            node = self.get_rand_node(tree)
            if node is None:
                continue
            self.stats['split'].n_trials += 1
            try:
                split_trees['trees'].extend(tree.split(node))
                split_trees['nodes'].append(node)
            except BaseException as err:
                self.stats['split'].n_failures += 1
                self.stats['split'].failed_inputs.append({'tree': tree, 'node': node, 'exception': str(err)})
        return split_trees

    def rejoin_trees(self, split_trees: dict) -> [AVLTree]:
        rejoined_trees = []
        for i in range(len(split_trees['nodes'])):
            left_subtree = split_trees['trees'][2*i]
            node = split_trees['nodes'][i]
            right_subtree = split_trees['trees'][2*i + 1]
            self.stats['join'].n_trials += 1
            try:
                rejoined_trees.append(left_subtree.join(right_subtree, node.get_key(), node.get_val()))
            except BaseException as err:
                self.stats['join'].n_failures += 1
                input = {
                    'left_subtree': left_subtree
                    , 'right_subtree': right_subtree
                    , 'node': node
                    , 'exception': str(err)
                }
                self.stats['join'].failed_inputs.append(input)
        return rejoined_trees

# -------------------------------- Validity Checkers -------------------------------- #
    def is_bst_valid(self, node, min_val=float('-inf'), max_val=float('inf')) -> bool:
        if not node.is_real_node():
            return True

        # Check if the current node key is within the valid range for BST
        if not (min_val < node.key < max_val):
            return False

        # Recursively check left and right subtrees with updated valid ranges
        return (self.is_bst_valid(node.left, min_val, node.key) and
                self.is_bst_valid(node.right, node.key, max_val))

    def is_avl_valid(self, root: AVLNode) -> bool:
        if not(root.is_real_node()):
            return True

        # Check AVL properties
        return (self.is_avl_valid(root.get_left()) and
                self.is_avl_valid(root.get_right()) and
                abs(root.get_balance_factor()) <= 1)

    def is_valid_tree(self, tree: AVLTree) -> bool:
        is_bst = self.is_bst_valid(tree.get_root())
        is_avl = self.is_avl_valid(tree.get_root())
        return is_bst and is_avl

    def get_validity_after(self, trees: [AVLTree], func_name: str):
        func_stats = self.stats[func_name]
        for tree in trees:
            if not self.is_valid_tree(tree):
                func_stats.n_invalid_trees += 1
                func_stats.invalid_trees.append(tree)
            if not self.is_size_valid(tree):
                func_stats.n_invalid_size += 1
                func_stats.invalid_size_trees.append(tree)
            if not self.is_min_valid(tree) or not self.is_max_valid(tree):
                func_stats.n_invalid_edge += 1
                func_stats.invalid_edge_trees.append(tree)

    def calc_tree_size(self, node: AVLNode) -> int:
        if not node.is_real_node():
            return 0

        left_size = self.calc_tree_size(node.get_left())
        right_size = self.calc_tree_size(node.get_right())
        return left_size + right_size + 1

    def is_size_valid(self, tree: AVLTree, size=0) -> bool:
        return tree.size == self.calc_tree_size(tree.get_root())

    @staticmethod
    def is_min_valid(self, tree: AVLTree) -> bool:
        if tree.size > 0:
            return tree.get_min() == tree.calc_min_node()
        return True

    @staticmethod
    def is_max_valid(tree: AVLTree):
        if tree.size > 0:
            return tree.get_max() == tree.calc_max_node()
        return True

# -------------------------------- Actual Tester -------------------------------- #
    def test(self):
        trees = self.build_trees_arr()
        self.get_validity_after(trees, func_name='insert')

        self.delete_rand_nodes(trees)
        self.get_validity_after(trees, func_name='delete')

        split_trees = self.split_trees(trees)
        self.get_validity_after(split_trees['trees'], func_name='split')

        rejoined_trees = self.rejoin_trees(split_trees)
        self.get_validity_after(rejoined_trees, func_name='join')

    def print_stats(self, resolution: int):
        for func_name in self.stats.keys():
            print(f'----stats for: {func_name}')
            func_stats = self.stats[func_name]
            failure_rate = round(func_stats.n_failures / max(func_stats.n_trials, 1), resolution)
            print(f'failure rate: {failure_rate}')
            print(f'invalid trees (avl & bst properties) rate: {round(func_stats.n_invalid_trees / self.n_trees, resolution)}')
            print(f'invalid tree size rate: {round(func_stats.n_invalid_size / self.n_trees, resolution)}')
            print(f'invalid tree max|min nodes rate: {round(func_stats.n_invalid_edge / self.n_trees, resolution)}')

    def get_failed_inputs(self, func_name: str) -> [dict]:
        assert func_name in FUNCS_NAMES
        return self.stats[func_name].failed_inputs

    def get_exceptions(self, func_name: str) -> [str]:
        inputs = self.get_failed_inputs(func_name)
        exceptions = [inp['exception'] for inp in inputs]
        return {err: exceptions.count(err) for err in exceptions}


tester = AVLTester(min_key=0, max_key=10**2, n_trees=10**2)
tester.test()
tester.print_stats(resolution=3)

pass
