from collections import deque
import math
from algorithm.visited_tracker import set_visited



def bfs_distance(start, target, map_data):
    #khảng cách min giữa 2 điểm =bfs
    if start == target:
        return 0
    
    # Xác định kích thước bản đồ và cách kiểm tra tường
    if hasattr(map_data, 'rows'):
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else:
        rows, cols = len(map_data), len(map_data[0])
        is_wall = lambda r, c: map_data[r][c] == 1

    queue = deque([(start, 0)])
    visited = {start}
    
    while queue:
        (curr_x, curr_y), dist = queue.popleft()
        
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = curr_x + dx, curr_y + dy
            
            if (nx, ny) == target:
                return dist + 1
            
            if (0 <= nx < rows and 0 <= ny < cols and
                not is_wall(nx, ny) and 
                (nx, ny) not in visited):
                
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    
    return 100 # Không tìm thấy đường đi


def euclid_distance(a, b):
    """Tính khoảng cách Euclid giữa 2 điểm."""
    return (
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2
    ) ** 0.5


def get_neighbors(pos, map_data, include_stay=True):
    """Lấy danh sách các vị trí lân cận hợp lệ."""
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    if include_stay:
        directions.append((0, 0))
        
    # Xác định kích thước bản đồ
    if hasattr(map_data, 'rows'): # Nếu là đối tượng Grid
        rows, cols = map_data.rows, map_data.cols
        is_wall = lambda r, c: map_data.cells[r][c] == 1
    else: # Nếu là mảng 2D (list of lists)
        rows, cols = len(map_data), len(map_data[0])
        is_wall = lambda r, c: map_data[r][c] == 1

    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if not is_wall(nx, ny):
                neighbors.append((nx, ny))
    return neighbors


# Heuristic wrappers for evaluate
def bfs_evaluate(pred_pos, prey_pos, map_data):
    return bfs_distance(pred_pos, prey_pos, map_data)

def euclid_evaluate(pred_pos, prey_pos, map_data):
    return euclid_distance(pred_pos, prey_pos)


# ----------------------------------------------------------------------


def minimax(map_data, pred_pos, prey_pos, depth, alpha, beta, is_maximizing, heuristic_fn, visited_nodes=None):

    if visited_nodes is None:
        visited_nodes = []

    if pred_pos == prey_pos:
        return -1000 # Predator bắt được Prey
    
    if depth == 0:
        return heuristic_fn(pred_pos, prey_pos, map_data)

    if is_maximizing:
        # Lượt của Prey (Maximizing)
        max_eval = -float('inf')
        for move in get_neighbors(prey_pos, map_data, include_stay=True):
            visited_nodes.append(move)
            eval_score = minimax(
                map_data, pred_pos, move, depth - 1, alpha, beta,
                False, heuristic_fn, visited_nodes=visited_nodes
            )
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval
    else:
        # Lượt của Predator (Minimizing)
        min_eval = float('inf')
        for move in get_neighbors(pred_pos, map_data, include_stay=False):
            visited_nodes.append(move)
            eval_score = minimax(
                map_data, move, prey_pos, depth - 1, alpha, beta,
                True, heuristic_fn, visited_nodes=visited_nodes
            )
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval


def get_predator_move(map_data, pred_pos, prey_pos, depth, heuristic_fn):
    """Tìm nước đi tối ưu cho Predator."""
    best_eval = float('inf')
    best_move = pred_pos
    visited_nodes = [pred_pos]   # Ghi lại các ô đã xem xét ở level 1
    score_map = {}
    
    for move in get_neighbors(pred_pos, map_data, include_stay=False):
        visited_nodes.append(move)
        eval_score = minimax(
            map_data, move, prey_pos, depth - 1, -float('inf'), float('inf'), True,
            heuristic_fn, visited_nodes=visited_nodes
        )
        score_map[move] = eval_score
        if eval_score < best_eval:
            best_eval = eval_score
            best_move = move

    set_visited(visited_nodes, [pred_pos, best_move], scores=score_map)
    return best_move


def get_prey_move(map_data, pred_pos, prey_pos, depth, heuristic_fn):
    """Tìm nước đi tối ưu cho Prey."""
    best_eval = -float('inf')
    best_move = prey_pos
    visited_nodes = [prey_pos]   # Ghi lại các ô đã xem xét ở level 1
    score_map = {}
    
    for move in get_neighbors(prey_pos, map_data, include_stay=True):
        visited_nodes.append(move)
        eval_score = minimax(
            map_data, pred_pos, move, depth - 1, -float('inf'), float('inf'), False,
            heuristic_fn, visited_nodes=visited_nodes
        )
        score_map[move] = eval_score
        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

    set_visited(visited_nodes, [prey_pos, best_move], scores=score_map)
    return best_move



# 1. Shortest Path (BFS)
def predator_minimax_shortest_path(map_data, pred_pos, prey_pos):
    return get_predator_move(map_data, pred_pos, prey_pos, depth=4, heuristic_fn=bfs_evaluate)

def prey_minimax_shortest_path(map_data, prey_pos, pred_pos):
    return get_prey_move(map_data, pred_pos, prey_pos, depth=4, heuristic_fn=bfs_evaluate)


# 2. Euclid
def predator_minimax_euclid(map_data, pred_pos, prey_pos):
    return get_predator_move(map_data, pred_pos, prey_pos, depth=4, heuristic_fn=euclid_evaluate)

def prey_minimax_euclid(map_data, prey_pos, pred_pos):
    return get_prey_move(map_data, pred_pos, prey_pos, depth=4, heuristic_fn=euclid_evaluate)

