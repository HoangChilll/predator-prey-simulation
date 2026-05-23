
from algorithm.greedy import predatorgreedy, preygreedy
from algorithm.random import random_move
from algorithm.dfs import predator_dfs_move,prey_dfs_move
from algorithm.A_hes import predator_move

ALGORITHMS = {
    "random": random_move,
    "p_greedy": predatorgreedy,
    "g_greedy": preygreedy,
    "p_dfs": predator_dfs_move,
    "g_dfs": prey_dfs_move,
    "p_A*": predator_move,
}
def selectAlgorithm(name):
    if name not in ALGORITHMS:
        raise ValueError(f"Algorithm '{name}' không tồn tại")
    return ALGORITHMS[name]
