import random
import time
import pandas as pd
from avl_template_new import AVLNode, AVLTree


# -------------------------------- Experimental Analysis -------------------------------- #
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


def experiment():
    res = {
        "exponent": []
        , "split_type": []
        , "n_joins": []
        , "total_time": []
        , "max_join_time": []
    }

    for exp in range(1, 11):
        print(f"Conducting experiment for n={1000 * 2 ** exp} ...")
        tree1, tree2 = generate_rand_trees(exp)
        res["exponent"].extend([exp, exp])

        random_split(tree1, res)
        max_split(tree2, res)

    return pd.DataFrame(res)


df = experiment()
print(df)
