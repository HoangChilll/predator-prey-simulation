
from algorithm.greedy import predatorgreedy, preygreedy
from algorithm.random import random_move
from algorithm.dfs import predator_dfs_move,prey_dfs_move
from algorithm.A_hes import predator_move
from algorithm.Khanhaphabeta import predator_minimax_shortest_path as khanh_predator_minimax, prey_minimax_shortest_path as khanh_prey_minimax
from algorithm.prey_A_star import prey_move
from algorithm.minimax_shortest_path import predator_minimax_shortest_path, prey_minimax_shortest_path
from algorithm.minimax_euclid import predator_minimax_euclid, prey_minimax_euclid

ALGORITHMS = {
    "random": random_move,

    # Predator algorithms
    "pred_greedy": predatorgreedy,
    "pred_dfs": predator_dfs_move,
    "pred_A*": predator_move,
    "pred_minimax_shortest": predator_minimax_shortest_path,
    "pred_minimax_euclid": predator_minimax_euclid,

    # Prey algorithms
    "prey_greedy": preygreedy,
    "prey_dfs": prey_dfs_move,
    "prey_A*": prey_move,
    "prey_minimax_shortest": prey_minimax_shortest_path,
    "prey_minimax_euclid": prey_minimax_euclid,
}
def selectAlgorithm(name):
    if name not in ALGORITHMS:
        raise ValueError(f"Algorithm '{name}' không tồn tại")
    return ALGORITHMS[name]
