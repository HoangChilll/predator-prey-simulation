from agents.strategies.bfs import PredatorBFS, PreyBFS
from agents.strategies.astar import PredatorAStar
# sau này thêm DFS, A*

def get_predator_strategy(name):
    if name == "bfs":
        return PredatorBFS()
    elif name == "dfs":
        return PredatorBFS()  # tạm thời
    elif name == "astar":
        return PredatorAStar()

def get_prey_strategy(name):
    if name == "bfs":
        return PreyBFS()
    elif name == "dfs":
        return PreyBFS()
    elif name == "astar":
        return PreyBFS()