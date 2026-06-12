
from algorithm.greedy import predator_greedy, prey_greedy
from algorithm.random import random_move
from algorithm.dfs import predator_dfs_move
from algorithm.predator_space_control import predator_space_control
from algorithm.prey_space_ap import prey_space_ap
from algorithm.prey_weighted_evade import prey_weighted_evade
from algorithm.minimax import (
    predator_minimax_shortest_path, prey_minimax_shortest_path,
    predator_minimax_euclid, prey_minimax_euclid,
)
from algorithm.prey_adaptive import prey_adaptive
from algorithm.A_star import predator_astar
from algorithm.bfs import predator_bfs

ALGORITHMS = {
    "random": random_move,

    # Predator algorithms
    "pred_greedy": predator_greedy,
    "pred_dfs": predator_dfs_move,
    "pred_bfs": predator_bfs,
    "pred_a_star": predator_astar,
    "pred_control": predator_space_control,
    "pred_minimax_shortest": predator_minimax_shortest_path,
    "pred_minimax_euclid": predator_minimax_euclid,

    # Prey algorithms
    "prey_greedy": prey_greedy,
    "pspaceap": prey_space_ap,
    "pweightedevade": prey_weighted_evade,
    "prey_adaptive": prey_adaptive,
    "pminimaxshortest": prey_minimax_shortest_path,
    "pminimaxeuclid": prey_minimax_euclid,
}
def selectAlgorithm(name):
    if name not in ALGORITHMS:
        raise ValueError(f"Algorithm '{name}' không tồn tại")
    return ALGORITHMS[name]


