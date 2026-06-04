
from algorithm.greedy import predatorgreedy, preygreedy
from algorithm.huyminimax import grey_minimax_shortest_path, prey_minimax_shortest_path
from algorithm.random import random_move
from algorithm.dfs import predator_dfs_move,prey_dfs_move
from algorithm.A_hes import predator_move
from algorithm.A_heugrey import grey_move
from algorithm.Khanhaphabeta import prey_minimax_shortest_path, grey_minimax_shortest_path
 

ALGORITHMS = {
    "random": random_move,
    "p_greedy": predatorgreedy,
    "g_greedy": preygreedy,
    "p_dfs": predator_dfs_move,
    "g_dfs": prey_dfs_move,
    "p_A*": predator_move,
    "huy_mi_prey": prey_minimax_shortest_path,
    "huy_mi_grey": grey_minimax_shortest_path,
    "grey_A*": grey_move,
    "K_mi_prey": prey_minimax_shortest_path,
    "K_mi_grey": grey_minimax_shortest_path
}
def selectAlgorithm(name):
    if name not in ALGORITHMS:
        raise ValueError(f"Algorithm '{name}' không tồn tại")
    return ALGORITHMS[name]
