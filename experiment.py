import random
from typing import Dict, List, Any

import pandas as pd
from avl_template_new import AVLTree, AVLNode


# -------------------------------- Experimental Analysis -------------------------------- #
def split(node) -> []:
    smaller_tree = AVLTree.tree_from_root(node.get_left())
    bigger_tree = AVLTree.tree_from_root(node.get_right())

    n_joins = 0  # delete me!!
    max_join_cost = 0  # delete me!!
    total_join_cost = 0

    parent = node.get_parent()
    while parent is not None:
        n_joins += 1  # delete me!!
        if node.is_left_son():
            right_subtree = AVLTree.tree_from_root(parent.get_right())
            join_cost = bigger_tree.join(right_subtree, parent.get_key(), parent.get_value())
        else:  # node is right son
            left_subtree = AVLTree.tree_from_root(parent.get_left())
            join_cost = left_subtree.join(smaller_tree, parent.get_key(), parent.get_value())
            smaller_tree.replace_tree(left_subtree)

        print(join_cost, n_joins)
        total_join_cost += join_cost
        if join_cost > max_join_cost:
            max_join_cost = join_cost

        parent.auto_reset_height()
        node = parent
        parent = node.get_parent()

    smaller_tree.fix_edges()
    bigger_tree.fix_edges()

    return [smaller_tree, bigger_tree], n_joins, max_join_cost, total_join_cost  # fix me!!


def generate_rand_trees(exp: int) -> (AVLTree, AVLTree):
    size = 1000 * 2 ** exp
    keys = [i for i in range(1, size + 1)]
    random.shuffle(keys)

    tree1 = AVLTree()
    tree2 = AVLTree()

    for key in keys:
        tree1.insert(key, key)
        tree2.insert(key, key)

    return tree1, tree2


def split_and_record(tree: AVLTree, node: AVLNode, res: dict, split_type: str):
    res["split_key"].append(node.key)
    res["depth"].append(tree.root.height - node.height)
    split_trees, n_joins, max_join_cost, total_join_cost = split(node)
    res["split_type"].append(split_type)
    res["n_joins"].append(n_joins)
    res["max_join_cost"].append(max_join_cost)
    res["total_join_cost"].append(total_join_cost)


def random_split(tree: AVLTree, res: dict) -> [AVLTree, AVLTree]:
    key = random.randint(1, tree.size + 1)
    node = tree.node_search(key)
    split_and_record(tree, node, res, split_type="random")


def max_split(tree: AVLTree, res: dict) -> [AVLTree, AVLTree]:
    node = tree.predecessor(tree.root)
    split_and_record(tree, node, res, split_type="max")


def experiment(n) -> dict[str, list[Any]]:
    res = {
        "exponent": []
        , "split_type": []
        , "split_key": []
        , "n_joins": []
        , "total_join_cost": []
        , "max_join_cost": []
        , "depth": []
    }

    for exp in range(1, n + 1):
        print(f"Conducting experiment for n={1000 * 2 ** exp} ...")
        tree1, tree2 = generate_rand_trees(exp)
        res["exponent"].extend([exp, exp])

        random_split(tree1, res)
        max_split(tree2, res)

    return res


def parse_results(res: dict) -> pd.DataFrame:
    df = pd.DataFrame(res)
    df["mean_cost_per_join"] = df["total_join_cost"] / df["n_joins"]
    df.drop(columns=["total_join_cost", "n_joins", "split_key", "depth"], inplace=True)

    rand = df[df["split_type"] == 'random']
    max_ = df[df["split_type"] == 'max']

    df = rand.merge(max_, how='inner', on='exponent', suffixes=('_rand', '_max'))
    df.drop(columns=['split_type_rand', 'split_type_max'], inplace=True)
    df = df.round(2)
    return df


df = parse_results(experiment(10))
df.to_excel('exp_res.xlsx')

pass
