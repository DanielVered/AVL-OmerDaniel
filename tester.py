import random
import time

import pandas as pd
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
        self.n_invalid_height = 0
        self.invalid_height_trees = []
        self.n_invalid_avl_to_array = 0
        self.invalid_avls_to_array = []


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
        arr = tree.avl_to_array()
        if len(arr) == 0:
            return None
        key = random.choice(arr)[0]
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
        trees = split_trees['trees']
        AVLTester.fix_sizes(trees)
        nodes = split_trees['nodes']
        for i in range(len(nodes)):
            left_subtree = trees[2*i]
            node = nodes[i]
            right_subtree = trees[2*i + 1]
            self.stats['join'].n_trials += 1
            try:
                left_subtree.join(right_subtree, node.get_key(), node.get_value())
                rejoined_trees.append(left_subtree)
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

    def validate_avl_to_array(self, trees: [AVLTree], func_name: str):
        func_stats = self.stats[func_name]
        for tree in trees:
            if tree.size != len(tree.avl_to_array()):
                func_stats.n_invalid_avl_to_array += 1
                func_stats.invalid_avls_to_array.append({'tree': tree, 'size': tree.size, 'array': tree.avl_to_array()})

    @staticmethod
    def fix_sizes(trees: [AVLTree]):
        for tree in trees:
            tree.size = AVLTester.calc_tree_size(tree.get_root())

# -------------------------------- Validity Checkers -------------------------------- #
    @staticmethod
    def is_bst_valid(node, min_val=float('-inf'), max_val=float('inf')) -> bool:
        if not node.is_real_node():
            return True

        # Check if the current node key is within the valid range for BST
        if not (min_val < node.key < max_val):
            return False

        # Recursively check left and right subtrees with updated valid ranges
        return (AVLTester.is_bst_valid(node.left, min_val, node.key) and
                AVLTester.is_bst_valid(node.right, node.key, max_val))

    @staticmethod
    def is_avl_valid(root: AVLNode) -> bool:
        if not(root.is_real_node()):
            return True

        # Check AVL properties
        return (AVLTester.is_avl_valid(root.get_left()) and
                AVLTester.is_avl_valid(root.get_right()) and
                abs(root.get_balance_factor()) <= 1)

    @staticmethod
    def is_valid_tree(tree: AVLTree) -> bool:
        is_bst = AVLTester.is_bst_valid(tree.get_root())
        is_avl = AVLTester.is_avl_valid(tree.get_root())
        return is_bst and is_avl

    def get_validity_after(self, trees: [AVLTree], func_name: str):
        func_stats = self.stats[func_name]
        for tree in trees:
            if not AVLTester.is_valid_tree(tree):
                func_stats.n_invalid_trees += 1
                func_stats.invalid_trees.append(tree)
            if not AVLTester.is_size_valid(tree):
                func_stats.n_invalid_size += 1
                func_stats.invalid_size_trees.append(tree)
            if not AVLTester.is_min_valid(tree) or not AVLTester.is_max_valid(tree):
                func_stats.n_invalid_edge += 1
                func_stats.invalid_edge_trees.append(tree)
            if not AVLTester.are_height_valid(tree.get_root()):
                func_stats.n_invalid_height += 1
                func_stats.invalid_height_trees.append(tree)


    @staticmethod
    def calc_tree_size(node: AVLNode) -> int:
        if not node.is_real_node():
            return 0

        left_size = AVLTester.calc_tree_size(node.get_left())
        right_size = AVLTester.calc_tree_size(node.get_right())
        return left_size + right_size + 1

    @staticmethod
    def is_size_valid(tree: AVLTree) -> bool:
        return tree.size == AVLTester.calc_tree_size(tree.get_root())

    @staticmethod
    def is_min_valid(tree: AVLTree) -> bool:
        return tree.get_min().get_key() == tree.calc_min_node().get_key()

    @staticmethod
    def is_max_valid(tree: AVLTree):
        return tree.get_max().get_key() == tree.calc_max_node().get_key()

    @staticmethod
    def are_height_valid(node: AVLNode):
        if not node.is_real_node():
            return node.height == -1

        return node.height == max(node.left.height, node.right.height) + 1

    @staticmethod
    def is_joinable(tree1, node, tree2):
        if not tree1.get_max().is_real_node() and not tree2.get_min().is_real_node():
            return True
        elif not tree1.get_max().is_real_node():
            return node.key < tree2.get_min().get_key()
        elif not tree2.get_min().is_real_node():
            return tree1.get_max().get_key() < node.key
        else:
            return tree1.get_max().get_key() < node.get_key() < tree2.get_min().get_key()

    # -------------------------------- Experimental Analysis -------------------------------- #
    @staticmethod
    def generate_rand_trees(exp: int) -> (AVLTree, AVLTree):
        size = 1000 * 2**exp
        keys = [i for i in range(1, size + 1)]
        random.shuffle(keys)

        tree1 = AVLTree()
        tree2 = AVLTree()

        for key in keys:
            tree1.insert(key, key)
            tree2.insert(key, key)

        return tree1, tree2

    @staticmethod
    def random_split(tree: AVLTree, res: dict) -> [AVLTree, AVLTree]:
        key = random.randint(1, tree.size)
        node = tree.node_search(key)
        # print("-- random: splitting on key:", node.key)

        start = time.time()
        split_trees, n_joins, max_join_time = tree.split(node)
        end = time.time()
        res["split_type"].append("random node")
        res["total_time"].append((end - start) * 10 ** 6)
        res["n_joins"].append(n_joins)
        res["max_join_time"].append(max_join_time)

    @staticmethod
    def max_split(tree: AVLTree, res: dict) -> [AVLTree, AVLTree]:
        node = tree.get_max()
        # print("-- max: splitting on key:", node.key)

        start = time.time()
        split_trees, n_joins, max_join_time = tree.split(node)
        end = time.time()
        res["split_type"].append("max node")
        res["total_time"].append((end - start) * 10 ** 6)
        res["n_joins"].append(n_joins)
        res["max_join_time"].append(max_join_time)

    @staticmethod
    def experiment():
        res = {
            "exponent": []
            , "split_type": []
            , "n_joins": []
            , "total_time": []
            , "max_join_time": []
        }

        for exp in range(1, 11):
            print(f"Conducting experiment for n={1000 * 2**exp} ...")
            tree1, tree2 = AVLTester.generate_rand_trees(exp)
            res["exponent"].extend([exp, exp])

            AVLTester.random_split(tree1, res)
            AVLTester.max_split(tree2, res)

        return pd.DataFrame(res)

    # -------------------------------- Actual Tester -------------------------------- #
    def test(self):
        trees = self.build_trees_arr()
        self.get_validity_after(trees, func_name='insert')
        self.validate_avl_to_array(trees, func_name='insert')

        self.delete_rand_nodes(trees)
        self.get_validity_after(trees, func_name='delete')
        self.validate_avl_to_array(trees, func_name='delete')

        split_trees = self.split_trees(trees)
        self.get_validity_after(split_trees['trees'], func_name='split')

        rejoined_trees = self.rejoin_trees(split_trees)
        self.get_validity_after(rejoined_trees, func_name='join')
        self.validate_avl_to_array(trees, func_name='join')

    def print_stats(self, resolution: int):
        for func_name in self.stats.keys():
            print(f'----stats for: {func_name}')
            func_stats = self.stats[func_name]
            failure_rate = round(func_stats.n_failures / max(func_stats.n_trials, 1), resolution)
            print(f'failure rate: {failure_rate}')
            print(f'invalid trees (avl & bst properties) rate: {round(func_stats.n_invalid_trees / self.n_trees, resolution)}')
            print(f'invalid tree size rate: {round(func_stats.n_invalid_size / self.n_trees, resolution)}')
            print(f'invalid tree max|min nodes rate: {round(func_stats.n_invalid_edge / self.n_trees, resolution)}')
            print(f'invalid tree heights rate: {round(func_stats.n_invalid_height / self.n_trees, resolution)}')
            print(f'invalid arrays rate: {round(func_stats.n_invalid_avl_to_array / self.n_trees, resolution)}')
            print(f"exceptions: \n  {self.get_exceptions(func_name)}")

    def get_failed_inputs(self, func_name: str) -> [dict]:
        assert func_name in FUNCS_NAMES
        return self.stats[func_name].failed_inputs

    def get_exceptions(self, func_name: str) -> [str]:
        inputs = self.get_failed_inputs(func_name)
        try:
            exceptions = [inp['exception'] for inp in inputs]
        except:
            exceptions = []
        return {err: exceptions.count(err) for err in exceptions}


# tester = AVLTester(min_key=0, max_key=10**2, n_trees=10**2)
# tester.test()
# tester.print_stats(resolution=3)

df = AVLTester.experiment()

pass
