
from algorithm.greedy import predatorgreedy, preygreedy
from algorithm.random import random_move
from algorithm.dfs import predator_dfs_move,prey_dfs_move

ALGORITHMS = {
    "random": random_move,
    "predator_greedy": predatorgreedy,
    "prey_greedy": preygreedy,
    "predator_dfs": predator_dfs_move,
    "prey_dfs": prey_dfs_move
}
def selectAlgorithm(name):
    if name not in ALGORITHMS:
        raise ValueError(f"Algorithm '{name}' không tồn tại")
    return ALGORITHMS[name]
